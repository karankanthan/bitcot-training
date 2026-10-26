# Task 2 Plan

## 1. Ticket Summary — Python
- Read the input CSV and inspect its columns and data quality.
- Count tickets by category and calculate average resolution time for valid, resolved tickets.
- Handle missing values, invalid dates, inconsistent category names, and malformed rows safely.
- Add tests for category counts, averages, and invalid or unresolved tickets.

## 2. SLA Checker — TypeScript
- Define SLA targets: urgent 4 hours, high 8 hours, normal 24 hours, and low 72 hours.
- Calculate elapsed hours between ticket creation and resolution.
- Report tickets that exceed their SLA and the amount of time exceeded.
- Add tests for tickets within the limit, exactly at the limit, and over the limit.

## 3. Debug Warm-up — Python
- Run the supplied script and compare its output with the expected result.
- Inspect the elapsed-time calculation and identify the root cause.
- Fix the calculation and verify the expected output.
- Add two lines explaining the bug and how it was identified.