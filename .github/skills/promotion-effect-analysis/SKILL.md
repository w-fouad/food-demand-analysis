---
name: promotion-effect-analysis
description: 'Analyze food-order promotion performance and أثر العروض الترويجية. Compare demand with and without email or homepage promotions using Mann-Whitney, and examine discount-demand relationships with Spearman. Use for عروض البريد، الحملات، الخصم، promotion, featured-meal, or offer-effect questions in this project.'
---

# Promotion Effect Analysis

Use this skill when a task asks whether promotion indicators or discounts are associated with food demand. It defines an analysis workflow; it does not assert that a promotion caused a change.

## Procedure

1. Use the prepared training dataset that contains `num_orders` and the promotion and price fields. Read source files without modifying them. Do not use `test.csv` as an orders outcome dataset because it has no `num_orders`.
2. Verify the input columns, row count, missing values, duplicate rows, and valid values for `emailer_for_promotion`, `homepage_featured`, `checkout_price`, `base_price`, and `num_orders`. State the actual dataset used.
3. Analyze `emailer_for_promotion` and `homepage_featured` separately. For each indicator, compare `num_orders` in its enabled and disabled groups. Follow the project requirement to compare observations for the same `meal_id` and `center_id` where both groups are represented, and use the Mann–Whitney U test.
4. For each comparison, report the group sample sizes, demand summaries, test statistic and p-value, and the observed effect size or percentage difference with its calculation stated. Explain that statistical significance is not proof of causality; note that offer exposure and discounts may be related.
5. Calculate the discount rate as `(base_price - checkout_price) / base_price` only where `base_price` is valid and nonzero. Report excluded invalid values and why. Use Spearman correlation to examine the monotonic association between discount rate and `num_orders`; report the sample size, coefficient, p-value, and direction.
6. Interpret results cautiously. Call out selection effects, repeated observations, unmeasured factors, and any test assumptions that limit interpretation. Do not generalize beyond the analyzed data.
7. Trace every reported number to the actual computation and preserve the source data. If a required field, comparison group, or verifiable result is unavailable, report that limitation rather than filling in a value.

## Expected Output

- Dataset and validated row count.
- Separate promotion-group comparisons with group sizes, demand summaries, Mann–Whitney results, and effect calculation.
- Discount-rate definition and Spearman results.
- Limitations that distinguish association from causal evidence.
