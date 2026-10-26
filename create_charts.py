"""Create four validated Food Demand Analysis charts."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, t as student_t


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "food_demand_train_merged.csv"
RAW_TRAIN_PATH = PROJECT_ROOT / "data" / "raw" / "train.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"
FIGURE_DPI = 300

REQUIRED_COLUMNS = {
    "week",
    "num_orders",
    "category",
    "emailer_for_promotion",
    "homepage_featured",
    "checkout_price",
    "base_price",
}


def _format_p_value(value: float, log10_value: float) -> str:
    if value == 0:
        if np.isfinite(log10_value):
            return f"< 1e-300 (log10 p = {log10_value:.1f})"
        return "< 1e-300"
    return f"{value:.3g}"


def main() -> None:
    if not DATA_PATH.is_file():
        raise FileNotFoundError(f"Prepared dataset not found: {DATA_PATH}")
    if not RAW_TRAIN_PATH.is_file():
        raise FileNotFoundError(f"Original training dataset not found: {RAW_TRAIN_PATH}")

    df = pd.read_csv(DATA_PATH)
    raw_train = pd.read_csv(RAW_TRAIN_PATH, usecols=["num_orders"])
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        raise ValueError(f"Prepared dataset is missing required columns: {missing_columns}")
    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required chart columns contain missing values.")
    if not df["num_orders"].map(np.isfinite).all():
        raise ValueError("num_orders contains non-finite values.")
    if not df["week"].map(np.isfinite).all():
        raise ValueError("week contains non-finite values.")
    if df["category"].astype(str).str.strip().eq("").any():
        raise ValueError("category contains empty values.")
    if not df["emailer_for_promotion"].isin([0, 1]).all():
        raise ValueError("emailer_for_promotion must contain only 0/1 values.")
    if not df["homepage_featured"].isin([0, 1]).all():
        raise ValueError("homepage_featured must contain only 0/1 values.")
    if len(df) != len(raw_train):
        raise AssertionError(
            f"Row count mismatch: prepared={len(df):,}, raw train={len(raw_train):,}"
        )

    prepared_orders = int(df["num_orders"].sum())
    raw_orders = int(raw_train["num_orders"].sum())
    if prepared_orders != raw_orders:
        raise AssertionError(
            f"num_orders mismatch: prepared={prepared_orders:,}, raw train={raw_orders:,}"
        )

    weekly_orders = df.groupby("week", sort=True)["num_orders"].sum()
    if weekly_orders.empty:
        raise ValueError("No weekly demand observations are available.")
    if weekly_orders.index.has_duplicates:
        raise AssertionError("Weekly aggregation returned duplicate week keys.")
    if int(weekly_orders.sum()) != prepared_orders:
        raise AssertionError("Weekly totals do not reconcile to the prepared dataset.")
    highest_week = weekly_orders.idxmax()
    lowest_week = weekly_orders.idxmin()

    category_orders = (
        df.groupby("category", sort=False)["num_orders"]
        .sum()
        .sort_values(ascending=False, kind="stable")
    )
    if int(category_orders.sum()) != prepared_orders:
        raise AssertionError("Category totals do not reconcile to the prepared dataset.")
    category_shares = category_orders / prepared_orders
    cumulative_category_share = category_shares.cumsum()
    categories_to_80 = int(np.searchsorted(cumulative_category_share.to_numpy(), 0.8) + 1)

    promoted = df["emailer_for_promotion"].eq(1) | df["homepage_featured"].eq(1)
    promotion_group = np.where(promoted, "مع أي ترويج", "دون ترويج")
    promotion_order = ["دون ترويج", "مع أي ترويج"]
    promotion_samples = {
        label: df.loc[promotion_group == label, "num_orders"].to_numpy()
        for label in promotion_order
    }
    if any(values.size == 0 for values in promotion_samples.values()):
        raise ValueError("Both promoted and non-promoted groups must have observations.")
    promotion_medians = {
        label: float(np.median(values))
        for label, values in promotion_samples.items()
    }

    base_price = df["base_price"].to_numpy(dtype=float)
    checkout_price = df["checkout_price"].to_numpy(dtype=float)
    valid_discount = (
        np.isfinite(base_price)
        & np.isfinite(checkout_price)
        & (base_price != 0)
    )
    excluded_discount_rows = int((~valid_discount).sum())
    discount_rate = (base_price[valid_discount] - checkout_price[valid_discount]) / base_price[
        valid_discount
    ]
    discount_orders = df.loc[valid_discount, "num_orders"].to_numpy(dtype=float)
    if discount_rate.size < 2:
        raise ValueError("At least two valid discount observations are required for Spearman.")
    spearman_result = spearmanr(discount_rate, discount_orders)
    if not np.isfinite(spearman_result.statistic):
        raise ValueError("Spearman correlation is undefined for the valid discount data.")
    spearman_t = spearman_result.statistic * np.sqrt(
        (len(discount_rate) - 2)
        / ((1 + spearman_result.statistic) * (1 - spearman_result.statistic))
    )
    spearman_log10_p = float(
        (np.log(2) + student_t.logsf(abs(spearman_t), len(discount_rate) - 2))
        / np.log(10)
    )

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    plt.rcParams["font.family"] = ["Tahoma", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    colors = {
        "blue": "#277DA1",
        "orange": "#F9844A",
        "slate": "#8D99AE",
        "dark": "#264653",
        "grid": "#D9DEE5",
    }

    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.plot(
        weekly_orders.index,
        weekly_orders.values,
        color=colors["blue"],
        linewidth=2.2,
        marker="o",
        markersize=3.2,
        markerfacecolor="white",
        markeredgewidth=1.1,
    )
    ax.scatter(
        [highest_week, lowest_week],
        [weekly_orders.loc[highest_week], weekly_orders.loc[lowest_week]],
        color=[colors["orange"], colors["slate"]],
        edgecolor="white",
        linewidth=1.2,
        s=100,
        zorder=4,
    )
    ax.annotate(
        f"أعلى أسبوع: {highest_week:g}\n{weekly_orders.loc[highest_week]:,.0f} طلب",
        (highest_week, weekly_orders.loc[highest_week]),
        xytext=(12, 16),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color=colors["dark"],
        arrowprops={"arrowstyle": "->", "color": colors["orange"]},
    )
    ax.annotate(
        f"أقل أسبوع: {lowest_week:g}\n{weekly_orders.loc[lowest_week]:,.0f} طلب",
        (lowest_week, weekly_orders.loc[lowest_week]),
        xytext=(12, 18),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color=colors["dark"],
        arrowprops={"arrowstyle": "->", "color": colors["slate"]},
    )
    ax.set_title("إجمالي الطلب يتغير أسبوعيًا مع قمم وقيعان واضحة", loc="right", pad=16, fontsize=15, fontweight="bold")
    ax.set_xlabel("الأسبوع (رقم تسلسلي)")
    ax.set_ylabel("إجمالي الطلبات (num_orders)")
    ax.grid(axis="y", color=colors["grid"], linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "weekly_demand_trend.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

    fig_width = max(10, len(category_orders) * 0.72)
    fig, ax = plt.subplots(figsize=(fig_width, 6.5))
    category_colors = [
        colors["blue"] if position < categories_to_80 else colors["slate"]
        for position in range(len(category_orders))
    ]
    bars = ax.bar(
        category_orders.index.astype(str),
        category_orders.values,
        color=category_colors,
        edgecolor="white",
        linewidth=0.7,
    )
    for position, bar in enumerate(bars):
        share = category_shares.iloc[position] * 100
        cumulative = cumulative_category_share.iloc[position] * 100
        if position < categories_to_80:
            ax.annotate(
                f"{share:.1f}%\nتراكمي {cumulative:.1f}%",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                rotation=0,
            )
    ax.set_title(
        f"أعلى {categories_to_80} فئات تكوّن {cumulative_category_share.iloc[categories_to_80 - 1] * 100:.1f}% من الطلب",
        loc="right",
        pad=16,
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("فئة الوجبة")
    ax.set_ylabel("إجمالي الطلبات (num_orders)")
    ax.tick_params(axis="x", labelrotation=35)
    ax.grid(axis="y", color=colors["grid"], linewidth=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "demand_by_category.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6.5))
    box_data = [promotion_samples[label] for label in promotion_order]
    box = ax.boxplot(
        box_data,
        tick_labels=[
            f"{label}\n(n={len(promotion_samples[label]):,})"
            for label in promotion_order
        ],
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "white", "linewidth": 2.3},
        whiskerprops={"color": colors["dark"], "linewidth": 1.2},
        capprops={"color": colors["dark"], "linewidth": 1.2},
        boxprops={"edgecolor": colors["dark"], "linewidth": 1.2},
    )
    for patch, color in zip(box["boxes"], [colors["slate"], colors["orange"]]):
        patch.set_facecolor(color)
        patch.set_alpha(0.88)
    ax.set_yscale("log")
    ax.set_title(
        "وسيط الطلب أعلى في الصفوف التي يظهر فيها أي ترويج",
        loc="right",
        pad=16,
        fontsize=14,
        fontweight="bold",
    )
    ax.set_xlabel("حالة الترويج (البريد أو الصفحة الرئيسية)")
    ax.set_ylabel("الطلب لكل صف (num_orders، مقياس لوغاريتمي)")
    for position, label in enumerate(promotion_order, start=1):
        ax.annotate(
            f"الوسيط = {promotion_medians[label]:,.0f}",
            (position, promotion_medians[label]),
            xytext=(8, 7),
            textcoords="offset points",
            fontsize=9,
            fontweight="bold",
            color=colors["dark"],
        )
    ax.grid(axis="y", which="both", color=colors["grid"], linewidth=0.7, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "promotion_vs_no_promotion.png",
        dpi=FIGURE_DPI,
        bbox_inches="tight",
    )
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(
        discount_rate * 100,
        discount_orders,
        s=10,
        alpha=0.16,
        color=colors["blue"],
        edgecolors="none",
        rasterized=True,
    )
    ax.set_title(
        f"علاقة الخصم بالطلب ضعيفة ({spearman_result.statistic:.3f}) ولا تثبت السببية",
        loc="right",
        pad=16,
        fontsize=14,
        fontweight="bold",
    )
    ax.set_yscale("log")
    ax.set_xlabel("نسبة الخصم = (السعر الأساسي − سعر البيع) ÷ السعر الأساسي (%)")
    ax.set_ylabel("الطلب لكل صف (num_orders، مقياس لوغاريتمي)")
    ax.text(
        0.02,
        0.98,
        f"Spearman ρ = {spearman_result.statistic:.4f}\n"
        f"p = {_format_p_value(float(spearman_result.pvalue), spearman_log10_p)}\n"
        f"n = {len(discount_rate):,}\n"
        f"صفوف مستبعدة من حساب الخصم = {excluded_discount_rows:,}",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "white", "edgecolor": colors["grid"], "alpha": 0.95},
    )
    ax.grid(color=colors["grid"], linewidth=0.7, alpha=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "discount_vs_demand.png", dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)

    expected_figures = [
        "weekly_demand_trend.png",
        "demand_by_category.png",
        "promotion_vs_no_promotion.png",
        "discount_vs_demand.png",
    ]
    for filename in expected_figures:
        image_path = FIGURES_DIR / filename
        if not image_path.is_file() or image_path.stat().st_size == 0:
            raise AssertionError(f"Chart was not saved correctly: {image_path}")

    print(f"Dataset: {DATA_PATH}")
    print(f"Rows: {len(df):,}; weekly observations: {len(weekly_orders):,}")
    print(f"Total orders (prepared): {prepared_orders:,}")
    print(f"Total orders (raw train.csv): {raw_orders:,}; row count and order sum match.")
    print(f"Highest-demand week: {highest_week:g} ({weekly_orders.loc[highest_week]:,} orders).")
    print(f"Lowest-demand week: {lowest_week:g} ({weekly_orders.loc[lowest_week]:,} orders).")
    print(
        f"Categories covering at least 80% of demand: {categories_to_80}; "
        f"cumulative share: {cumulative_category_share.iloc[categories_to_80 - 1] * 100:.2f}%."
    )
    print(
        "Promotion comparison uses rows with either email promotion or homepage feature: "
        f"n_without={len(promotion_samples[promotion_order[0]]):,}, "
        f"median_without={promotion_medians[promotion_order[0]]:,.0f}; "
        f"n_with={len(promotion_samples[promotion_order[1]]):,}, "
        f"median_with={promotion_medians[promotion_order[1]]:,.0f}."
    )
    print(
        f"Discount: {len(discount_rate):,} valid rows, {excluded_discount_rows:,} excluded; "
        f"Spearman rho={spearman_result.statistic:.6f}, "
        f"p={_format_p_value(float(spearman_result.pvalue), spearman_log10_p)}."
    )
    print("Promotion association is descriptive; correlation does not establish causation.")
    for filename in expected_figures:
        image_path = FIGURES_DIR / filename
        print(f"Saved {image_path} ({image_path.stat().st_size:,} bytes, {FIGURE_DPI} DPI).")


if __name__ == "__main__":
    main()
