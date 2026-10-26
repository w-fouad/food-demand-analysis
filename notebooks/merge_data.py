"""Merge the training data with meal and fulfillment-center metadata."""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "food_demand_train_merged.csv"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames is None:
            raise ValueError(f"{path.name} has no header row")
        return reader.fieldnames, list(reader)


def count_missing(rows: list[dict[str, str]], columns: list[str]) -> int:
    return sum(
        value is None or value.strip() == ""
        for row in rows
        for value in (row.get(column) for column in columns)
    )


def count_duplicate_rows(
    rows: list[dict[str, str]], columns: list[str]
) -> int:
    seen: set[tuple[str | None, ...]] = set()
    duplicates = 0
    for row in rows:
        row_values = tuple(row.get(column) for column in columns)
        if row_values in seen:
            duplicates += 1
        else:
            seen.add(row_values)
    return duplicates


def make_lookup(
    name: str, rows: list[dict[str, str]], key: str
) -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}
    for row in rows:
        value = row[key]
        if value is None or value.strip() == "":
            raise ValueError(f"{name} contains an empty {key}")
        if value in lookup:
            raise ValueError(f"{name} contains duplicate {key}={value}")
        lookup[value] = row
    return lookup


def main() -> None:
    train_columns, train_rows = read_csv(RAW_DIR / "train.csv")
    center_columns, center_rows = read_csv(
        RAW_DIR / "fulfilment_center_info.csv"
    )
    meal_columns, meal_rows = read_csv(RAW_DIR / "meal_info.csv")

    required_train_columns = {"center_id", "meal_id", "num_orders"}
    if not required_train_columns.issubset(train_columns):
        raise ValueError("train.csv is missing required merge or target columns")
    if "center_id" not in center_columns or "meal_id" not in meal_columns:
        raise ValueError("A metadata file is missing its merge key")

    center_lookup = make_lookup("fulfilment_center_info.csv", center_rows, "center_id")
    meal_lookup = make_lookup("meal_info.csv", meal_rows, "meal_id")
    merged_columns = (
        train_columns
        + [column for column in center_columns if column != "center_id"]
        + [column for column in meal_columns if column != "meal_id"]
    )

    rows_before = len(train_rows)
    orders_before = sum(int(row["num_orders"]) for row in train_rows)
    duplicates_before = count_duplicate_rows(train_rows, train_columns)
    missing_before = count_missing(train_rows, train_columns)

    merged_rows: list[dict[str, str]] = []
    unmatched_centers: set[str] = set()
    unmatched_meals: set[str] = set()
    for row in train_rows:
        center = center_lookup.get(row["center_id"])
        meal = meal_lookup.get(row["meal_id"])
        if center is None:
            unmatched_centers.add(row["center_id"])
        if meal is None:
            unmatched_meals.add(row["meal_id"])
        if center is not None and meal is not None:
            merged_rows.append(
                {
                    **row,
                    **{key: value for key, value in center.items() if key != "center_id"},
                    **{key: value for key, value in meal.items() if key != "meal_id"},
                }
            )

    if unmatched_centers or unmatched_meals:
        raise ValueError(
            "Merge stopped: unmatched keys; "
            f"center_id={sorted(unmatched_centers)}, meal_id={sorted(unmatched_meals)}"
        )

    rows_after = len(merged_rows)
    orders_after = sum(int(row["num_orders"]) for row in merged_rows)
    duplicates_after = count_duplicate_rows(merged_rows, merged_columns)
    missing_after = count_missing(merged_rows, merged_columns)

    print(f"Rows before merge (train.csv): {rows_before}")
    print(f"Sum of num_orders before merge: {orders_before}")
    print(f"Full duplicate rows before merge: {duplicates_before}")
    print(f"Missing cells before merge: {missing_before}")
    print(f"Rows after merge: {rows_after}")
    print(f"Sum of num_orders after merge: {orders_after}")
    print(f"Full duplicate rows after merge: {duplicates_after}")
    print(f"Missing cells after merge: {missing_after}")
    print(f"Unmatched center_id keys: {len(unmatched_centers)}")
    print(f"Unmatched meal_id keys: {len(unmatched_meals)}")

    if rows_after != rows_before or orders_after != orders_before:
        raise ValueError(
            "Merge stopped before saving: row count or num_orders sum changed"
        )
    if duplicates_after > duplicates_before:
        raise ValueError(
            "Merge stopped before saving: full duplicate rows increased"
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as destination:
        writer = csv.DictWriter(destination, fieldnames=merged_columns)
        writer.writeheader()
        writer.writerows(merged_rows)

    print(f"Saved merged data to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
