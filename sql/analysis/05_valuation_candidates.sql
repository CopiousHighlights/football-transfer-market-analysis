-- Exploratory model gap; not proof of undervaluation.
SELECT player_name,position,current_club_name,tm_value,fair_value,
  ROUND(fair_value-tm_value,2) AS model_gap_eur,
  ROUND(1.0*tm_value/NULLIF(fair_value,0),3) AS listed_to_model_ratio
FROM valuation_sample WHERE minutes>=900 AND fair_value>0
ORDER BY model_gap_eur DESC LIMIT 20;
