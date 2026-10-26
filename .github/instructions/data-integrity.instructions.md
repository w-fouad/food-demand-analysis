---
name: "Data Integrity Rule"
description: "Use when reading, cleaning, merging, or deleting food-demand data; protect original data/raw files, validate row counts and num_orders totals, and document cleaning decisions."
---
applyTo: "notebooks/**,reports/**,docs/**,README.md"
---

# Data Integrity Rule

- Treat every file in `data/raw/` as an immutable original: read it only. Never edit, overwrite, delete, or regenerate source files there.
- Never include `data/` or its contents in GitHub uploads.
- Before and after every merge or deletion, record the row count. After a merge, also compare the `num_orders` sum before and after. Investigate and report any change; do not conceal it or accept the output as valid until its cause is understood.
- Check merge keys, unmatched records, and key cardinality so joins do not silently duplicate or drop observations.
- Document each data-cleaning decision and its reason in `docs/cleaning_decisions`. Report observed issue counts and retain source data; do not silently remove or overwrite records.
