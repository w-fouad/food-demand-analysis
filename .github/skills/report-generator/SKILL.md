---
name: report-generator
description: "Prepare and review the Food Demand Analysis client report, README, and presentation in Arabic. Use when summarizing verified findings, preparing recommendations, or documenting project limitations."
metadata:
  source: "https://skills.sh/claude-office-skills/skills/report-generator"
  upstream: "https://github.com/claude-office-skills/skills/tree/main/report-generator"
  upstream-license: MIT
---

# Client Report Generator

Turn the current, verified analysis into a clear client report and matching project documentation. Do not create or imply results that have not been computed.

## Procedure

1. Review the current analysis notebook, its latest outputs, and the referenced figures before drafting. If execution failed or a result is missing, state the limitation instead of filling it in.
2. Write in Arabic and keep original filenames and column names unchanged. Follow the project's required delivery paths and formats.
3. Start the client report with an executive summary of exactly five lines, beginning with the most important verified finding and its value.
4. Answer the project questions using computed values and relevant charts. Trace each reported number to a current analysis output.
5. Give at least three recommendations. For each, state the proposed action, the measured result supporting it, and a measurable success indicator. Do not claim guaranteed savings or operational impact.
6. Include clear analysis limitations: weeks do not provide actual calendar dates, city identifiers are coded, the data lacks inventory and waste observations, and association does not establish causation.
7. Verify that every referenced figure exists in `reports/figures/` and that each filename and link is correct.
8. Keep the report, `README.md`, and presentation consistent. Cover the problem, data and quality, findings, recommendations, limitations, and use of AI where requested.
9. Recheck every figure, percentage, and claim against the actual analysis before delivery. Remove unsupported or stale numbers.

## Expected Output

- Arabic client report with a five-line executive summary, findings, recommendations, evidence, and limitations.
- README and presentation consistent with the verified report.
- Valid links to existing project figures and reproducible analysis outputs.
