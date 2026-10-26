---
name: data-visualization
description: "Choose, create, and review quantitative charts for the Food Demand Analysis project. Use for weekly trends, category and center comparisons, promotion groups, discount relationships, demand volatility, or PNG figure review."
metadata:
  source: "https://skills.sh/anthropics/knowledge-work-plugins/data-visualization"
  upstream: "https://github.com/anthropics/knowledge-work-plugins/tree/main/data/skills/data-visualization"
  upstream-license: Apache-2.0
---

# Data Visualization

Create accurate, readable charts that answer a stated project question and agree with the calculations in the analysis.

## Procedure

1. Identify the question, population, time period, aggregation level, units, and denominator before choosing a chart.
2. Match the chart to the evidence: line for weekly trends, ordered bars for category or center comparisons, box plots for demand distributions, and scatter plots for discount-demand relationships.
3. Use Arabic titles and axis labels. Make the title state the supported takeaway when results are known; do not write a conclusion before checking the computed values.
4. Distinguish sums, averages, rates, and row counts. Label denominators and sample sizes when they affect interpretation. Avoid misleading axis ranges and unnecessary dual axes, 3D effects, or pie charts for many categories.
5. Use a restrained, accessible color palette and more than color alone to distinguish groups. Preserve original data and column names.
6. Export at least four project figures as PNG files under `reports/figures/`. Use actual analysis output rather than manually entered values.
7. Inspect each exported image for legible text, unclipped labels, correct units, and consistency with the reported result.
8. Describe observational comparisons and correlations accurately. A chart does not prove causality.

## Expected Output

- A chart linked to a specific question and an actual calculation.
- Arabic title, labeled axes, correct aggregation, units, and denominators.
- PNG figure saved under `reports/figures/` and checked after export.
