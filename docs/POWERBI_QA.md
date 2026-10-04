# Power BI Desktop verification

Open power-bi/TransferMarket.pbip, select Refresh, and verify that all three pages render.
On the summer page, the unfiltered record count should be 1,493 and positive reported fee coverage should be 499 / 1,493 (33.4%).
Destination-league selections should update all summer cards and charts. League totals should match analysis/01_league_arrivals.csv.
Check that permanent fees exclude loans, unknown fees remain blank, and the historical EUR page does not affect summer GBP totals.
Historical records should be 200 and valuation records 150. These are selected samples.
Check readable titles, table columns, currency formats and date labels at normal zoom.
Set ProjectRoot to the cloned repository path to use file refresh; blank uses the bundled snapshot.
Save the verified report as a PBIX, capture actual screenshots and update the README validation status.

Current limitation: native Desktop automation is unavailable in this session, so these interaction and rendering checks are pending.
