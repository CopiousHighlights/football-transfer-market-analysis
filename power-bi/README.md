# Power BI report

Open `TransferMarket.pbip` with Power BI Desktop, then choose Refresh. The native report has three pages,
12 DAX measures, typed Power Query imports, and two dimension-to-fact relationships.
Blank ProjectRoot uses an embedded copy of the processed CSV snapshot so the project is portable.
To refresh from your files, run the Python pipeline, set the ProjectRoot parameter to your repository folder
(use forward slashes), and refresh Power BI. Embedded snapshots remain unchanged until regenerated.

The report is authored as PBIP/PBIR and TMSL model files, not a PBIX binary.
Definition files are checked against Microsoft schemas; native Desktop visual rendering and DAX execution
must be verified before describing the dashboard as fully tested. No screenshot here is claimed to be a Desktop capture.

Summer fee metrics exclude loans and never mix GBP with EUR. Destination-league filters apply to the
summer page. Historical and valuation pages use independent selected samples.
See `../docs/METHODOLOGY.md` for missing sources and interpretation limits.

Format reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report
Model reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset
