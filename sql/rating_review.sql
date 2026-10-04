-- Editorial scores, kept separate from measured transfer facts.
SELECT player_name,to_club,transfer_date,fee_amount,currency,rating,
       rating_status,role,rationale
FROM transfer_ratings
WHERE rating IS NOT NULL
ORDER BY rating DESC,player_name,transfer_date;

-- Compare only within currency and dataset; this is not a market ranking.
SELECT dataset,currency,rating_status,COUNT(*) AS deals,
       ROUND(AVG(rating),1) AS mean_editorial_rating
FROM transfer_ratings
GROUP BY dataset,currency,rating_status;
