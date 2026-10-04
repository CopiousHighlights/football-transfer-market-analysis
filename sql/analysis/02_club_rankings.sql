-- CTE + window function: compare buyers within each destination league.
WITH ranked AS (
  SELECT *, DENSE_RANK() OVER (PARTITION BY league ORDER BY reported_permanent_fees_gbp DESC) AS league_spend_rank
  FROM v_club_buying
  WHERE league IN ('Premier League','La Liga','Serie A','Bundesliga','Ligue 1')
) SELECT * FROM ranked WHERE league_spend_rank<=5 ORDER BY league,league_spend_rank;
