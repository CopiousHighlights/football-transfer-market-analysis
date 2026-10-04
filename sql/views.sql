-- Grain: one source transfer record, not one unique player.
CREATE VIEW IF NOT EXISTS v_league_arrivals AS
SELECT to_league AS league, COUNT(*) AS transfers,
       SUM(is_permanent_fee) AS permanent_reported_fee_deals,
       SUM(CASE WHEN is_permanent_fee=1 THEN quoted_fee_gbp ELSE 0 END) AS reported_permanent_fees_gbp,
       SUM(CASE WHEN quoted_fee_gbp IS NULL THEN 1 ELSE 0 END) AS missing_fee_rows
FROM summer_transfers
WHERE to_league IN ('Premier League','La Liga','Serie A','Bundesliga','Ligue 1')
GROUP BY to_league;
CREATE VIEW IF NOT EXISTS v_club_buying AS
SELECT to_club AS club, to_league AS league, COUNT(*) AS transfers,
       SUM(CASE WHEN is_permanent_fee=1 THEN quoted_fee_gbp ELSE 0 END) AS reported_permanent_fees_gbp
FROM summer_transfers GROUP BY to_club,to_league;
