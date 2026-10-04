-- Aggregate components before joining to avoid multiplying transfer records.
WITH component_counts AS (
  SELECT record_id,COUNT(*) AS component_count FROM fee_components GROUP BY record_id
) SELECT t.record_id,t.player_name,t.quoted_fee_gbp,t.quote_basis,c.component_count
FROM summer_transfers t JOIN component_counts c ON t.record_id=c.record_id
ORDER BY c.component_count DESC,t.record_id;
