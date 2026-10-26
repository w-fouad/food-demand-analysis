---
name: demand-kpi-analysis
description: 'Calculate and validate food-demand KPIs from project data, including weekly order totals, num_orders, meal and category shares, center performance, and demand volatility. Use for مؤشرات الطلب، الطلب الأسبوعي، تذبذب الطلب، demand metrics, weekly trends, top meals, category analysis, or center comparisons.'
---

# Demand KPI Analysis

Use this skill to calculate descriptive demand measures for the food-demand project from observed data. Do not substitute estimates for computed metrics.

## Procedure

1. Load the prepared training data with `num_orders` and the required meal and center metadata. Do not modify source files. Do not calculate demand outcomes from `test.csv`, which has no `num_orders`.
2. Before calculating KPIs, check required columns, row count, missing values, duplicate rows, key coverage, and numeric validity of `num_orders`. Record the dataset and any documented exclusions.
3. Calculate total orders and weekly total orders using `week`; report the observed week range and check for missing weeks before describing a trend.
4. Aggregate orders by meal category and by meal. Report totals and shares of total orders. Rank in descending order and identify the smallest prefix of ranked items whose cumulative share reaches at least 80%, if that concentration analysis is requested.
5. Aggregate orders by fulfillment center and compare centers by observed totals and average weekly demand. Summarize center performance by `center_type` where the metadata is available. State the aggregation and time coverage so unequal coverage is not mistaken for performance.
6. Measure meal-demand volatility by first aggregating weekly orders at the stated meal scope, then calculating standard deviation divided by mean (coefficient of variation). State the scope and period; flag a zero or undefined mean rather than reporting an invalid ratio.
7. If revenue or discount KPIs are requested, define them explicitly before calculation: revenue is `checkout_price * num_orders`; discount rate is `(base_price - checkout_price) / base_price` for valid nonzero base prices. Do not label revenue as profit.
8. Validate reported totals against the input, make units and denominators explicit, and trace every number to its calculation. Do not invent figures, silently drop records, or claim that an observed association proves causality.

## Expected Output

- Input validation summary and dataset scope.
- Weekly totals and the requested meal, category, center, or center-type KPIs.
- Explicit formulas, denominators, and aggregation levels.
- Volatility results with the period and scope.
- Data limitations and verifiable sources for every reported figure.
