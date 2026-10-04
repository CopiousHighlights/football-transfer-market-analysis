# How to explain the project

Start with the question: which leagues and clubs dominate reported transfer fees, and how does missing disclosure affect what we can conclude?
Open Excel to show the source, then src/pipeline.py to show extraction and validation. Show SQL query 02 for ranking buyers within a league and query 06 for avoiding join duplication.
Explain that an undisclosed fee is unknown, not zero. A free transfer also does not imply zero wages or agent costs.
Explain that a within-top-five transfer can be an arrival and departure, but remains one transfer record.
Show how Power Query converts types and DAX uses the current league filter. Keep the sample pages separate from summer metrics.
Describe fair_value as an existing estimate whose code is unavailable; do not claim to have trained a model or verified undervaluation.
Discuss the missing full dataset openly, then describe improvements: independently check disputed fees, obtain model code, add versioned source refreshes and complete Desktop QA.

Suggested resume wording after reviewing and understanding the implementation:
“Built an Excel-to-Python/SQLite analytics pipeline for 1,493 football transfer records, using SQL CTEs and window functions, null-aware fee metrics, reconciliation checks and automated GitHub validation; authored a three-page Power BI report project with Power Query and DAX.”
Add ‘validated interactive dashboard’ only after testing it in Power BI Desktop.
