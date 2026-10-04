# Source, scope and metric definitions

The Excel workbook is the provided source snapshot. It is retained byte-for-byte.
Summer26_New and Summer26_Matches form the summer analytical dataset: one source record per transfer.
Summer26_Review remains separate and is excluded from the dashboard. Matches are included once here;
the historical Paid_Sample is never appended to this fact table.

**Reported permanent fees (GBP)** sum positive quoted_fee_gbp for transfer_type = Fee.
These are quoted amounts, sometimes including add-ons, not audited expenditure.
**Reported fee coverage** is positive numeric fee records divided by transfer records.
Free transfers and undisclosed/unknown fees remain distinct. Blank fees never become zero.
Loans are excluded from permanent fee sums. Fee_Components is explanatory detail and is not added to quoted totals.
Arrivals count destination leagues; departures count origin leagues. A transfer between two top-five leagues
appears in both views, so arrivals and departures must not be added into a transfer count.

Announcement dates are source dates, not registration dates. Source summer coverage includes early
announcements and later exits. Historic Paid_Sample is a selected 200-row high-fee sample in EUR;
FTV_Worth is a selected 150-row valuation sample. Neither represents the entire market.
GBP and EUR are never summed together. The full 175,182-row dataset mentioned by the workbook is not supplied.
Existing summary totals and fair_value estimates cannot be independently reproduced from the supplied samples.
No valuation model is invented or claimed to have been trained.

Data is described by the owner as real-world. Source links are retained per record. Some fees conflict across
reports (see Source_Checks). Source-reported transfers require independent verification before presenting
them as authoritative market facts. Conclusions below describe this workbook snapshot.

Main tracker: https://www.theguardian.com/football/ng-interactive/2026/sep/01/mens-transfer-window-summer-2026-all-deals-from-europes-top-five-leagues
Source snapshot retrieved: 3 October 2026.
This project is independently created; it is not affiliated with Transfermarkt or any club.
Source data retains its original ownership; no blanket data redistribution license is asserted.
