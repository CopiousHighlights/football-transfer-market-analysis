-- Announcement timing is not registration timing; no imposed window cutoffs.
SELECT announcement_month,COUNT(*) AS transfers,
  SUM(CASE WHEN is_permanent_fee=1 THEN quoted_fee_gbp ELSE 0 END) AS reported_permanent_fees_gbp
FROM summer_transfers GROUP BY announcement_month ORDER BY announcement_month;
