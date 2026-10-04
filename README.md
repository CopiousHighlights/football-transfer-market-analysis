# Football Transfer Market Analysis

[![Validate analysis](https://github.com/CopiousHighlights/football-transfer-market-analysis/actions/workflows/validate.yml/badge.svg)](https://github.com/CopiousHighlights/football-transfer-market-analysis/actions/workflows/validate.yml)

An Excel-led football analytics project that turns a documented workbook snapshot into reproducible Python processing, SQL analysis, and a native Power BI report project.

**Business question:** How do reported transfer fees, buying patterns, and fee disclosure vary across clubs, leagues, and positions—and what can the available data actually support?

## Start here

- **[Excel workbook](excel/Football_Transfer_Worth_Final.xlsx)** — original final workbook, preserved unchanged.
- **[Power BI project](power-bi/TransferMarket.pbip)** — download/clone the entire repository, open in Power BI Desktop, and refresh. Three pages and 12 DAX measures; Desktop validation remains pending.
- **[SQL analysis](sql/analysis/)** — six queries covering league arrivals, club rankings, large reported fees, announcement timing, valuation gaps, and component joins.
- **[Python pipeline](src/pipeline.py)** — extracts the workbook, preserves nulls, builds SQLite and CSVs, runs SQL, and reconciles results.
- **[Methodology](docs/METHODOLOGY.md)** — metric definitions, source links, currency rules, and limitations.

## What this snapshot shows

The analytical summer dataset contains **1,493 transfer records**: 1,475 additions plus 18 workbook matches, each included once. Another 28 records remain excluded/reviewed separately.
**499 records (33.4%) have positive quoted fees.** The remaining records include free, undisclosed, and other non-numeric fee statuses; missing fees are not evidence of zero spending.
The destination-league breakdown in [SQL results](analysis/01_league_arrivals.csv) identifies the Premier League as the largest recipient of reported permanent fees in this snapshot.

These are source-snapshot findings, not independently verified market totals. Reported quotes may include add-ons. The project does not combine GBP and EUR or add component amounts to quoted totals.

## Skills demonstrated

| Tool | Concrete work |
| --- | --- |
| Excel | Existing formulas, data dictionary, fee samples, quality summaries, charts and formatted tables |
| Python | Typed extraction, CSV exports, SQLite loading, source fingerprints, reconciliation and tests |
| SQL / SQLite | Aggregations, CTEs, DENSE_RANK, NULLIF, views and joins that avoid duplicate totals |
| Power Query | Portable snapshot import, optional file refresh, null handling and explicit column types |
| DAX | Filter-aware counts, reported fee sums, coverage, median and exploratory model gaps |
| Data modeling | Transfer fact with destination-league and announcement-date dimensions; independent sample tables |
| Git / GitHub Actions | Versioned analysis and automated pipeline validation |

## Reproduce the analysis

Requires Python 3.10+.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python src/pipeline.py
python src/build_powerbi.py
python -m unittest discover -s tests -v
```

Outputs: `data/processed/*.csv`, `data/transfer_market.sqlite`, `analysis/*.csv`, and `analysis/quality_report.json`.
The SQLite database is included so SQL can be explored immediately in a database client.
Pipeline reruns rebuild the outputs from the Excel workbook. They do not overwrite Excel.
Power BI refresh instructions are in [power-bi/README.md](power-bi/README.md).
`python src/build_powerbi.py` rebuilds the portable report snapshot from the processed CSVs.

## Report pages

1. **Summer 2026:** transfer records, reported permanent fees (GBP), disclosure coverage, destination-league slicer, position/fee-status breakdowns, announcement timing and transfer detail.
2. **Historical sample:** selected 200 high-fee records, fee sum and median (EUR), positions, club filtering and player detail.
3. **Valuation sample:** 150 existing model estimates, listed values, model gap by position and player detail. Exploratory; not a validated valuation model.

## Validation and remaining work

Python/SQL checks pass for unique transfer IDs, source-status partition, non-negative fees, fee-component references, destination-league counts and independent fee-total reconciliation. Six automated tests cover those checks, unknown fees, join duplication, portable report snapshots and report field bindings.
The 27 native Power BI report JSON files pass Microsoft's public schema checks. Report definitions, relationships and DAX are included; **visual rendering, filter interactions and DAX execution in Power BI Desktop have not yet been tested**. No PBIX binary or native dashboard screenshot is claimed.
After Desktop validation, save a PBIX and add actual report screenshots to this repository for a stronger recruiter handoff.

The full 175,182-row historical dataset and code behind `fair_value` are not supplied. Full-market workbook summaries and valuation accuracy cannot be independently reproduced. The historical and valuation samples must not be presented as the full market.

## Structure

```text
excel/           Final source workbook
src/             Reproducible Python pipeline
sql/             SQL views and analytical queries
data/            Processed CSVs and SQLite database
analysis/        Query results and quality evidence
power-bi/        PBIP/PBIR report, semantic model, Power Query and DAX
docs/            Methodology and interview walkthrough
tests/           Analytical correctness tests
.github/         Continuous integration
```

## Source and ownership

Workbook supplied by the project owner. Summer source links are retained in row-level data; snapshot date: 3 October 2026. See [methodology](docs/METHODOLOGY.md).
This independent portfolio project is not affiliated with Transfermarkt, the source publishers, or any football club. Data retains its original ownership; this repository does not grant a blanket license for third-party data.
