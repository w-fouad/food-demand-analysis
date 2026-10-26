---
name: demand-forecasting
description: "Forecast weekly meal demand for the Food Demand Analysis project. Use when evaluating Linear Regression or Random Forest forecasts, temporal validation, MAE, or the previous-week baseline."
metadata:
  source: "https://skills.sh/finsilabs/awesome-ecommerce-skills/demand-forecasting"
  upstream: "https://github.com/finsilabs/awesome-ecommerce-skills/tree/main/skills/business-operations/demand-forecasting"
  upstream-license: MIT
---

# Demand Forecasting

Apply the forecasting workflow to the project's observed weekly meal demand. Forecasts support planning; they do not establish actual inventory needs without stock, waste, and lead-time data.

## Procedure

1. Read the project instructions and inspect the available columns and week coverage. Keep `data/raw/` unchanged and exclude it from GitHub.
2. Use `num_orders` from the training data as the observed outcome. Do not treat `test.csv` as labeled data; it has no `num_orders`.
3. Build a reproducible time-ordered validation that holds out the latest 10 training weeks. Do not randomly shuffle rows across the time boundary or let validation targets leak into features.
4. If modeling is requested, train a Linear Regression or Random Forest model using features available at prediction time. Document the feature set and any encoding or preprocessing.
5. Create a previous-week forecast baseline at the same meal and center grain. Ensure the prior week's actual values are available for each forecasted observation; document missing prior-week observations rather than inventing substitutes.
6. Calculate and report MAE on the same held-out observations for the model and baseline. Include sample size, units, week range, and the MAE calculation. Do not report a comparison if the evaluated rows differ without explaining why.
7. For the optional `test.csv` forecast, fit the chosen model only on appropriate labeled training data and explain that test predictions cannot be scored because test labels are unavailable.
8. State limitations, including the lack of inventory, waste, actual calendar dates, and supplier lead times when relevant. Never translate a demand forecast into an unverified claim about stockouts or savings.

## Expected Output

- Time-based split and feature definition.
- Model and previous-week baseline MAE on the same validation records.
- Test-set prediction scope and the absence of test labels for scoring.
- Explicit limitations and links to reproducible calculations.
