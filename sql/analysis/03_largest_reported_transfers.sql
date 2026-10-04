SELECT record_id,player_name,from_club,to_club,to_league,quoted_fee_gbp,quote_basis,source_url
FROM summer_transfers WHERE is_permanent_fee=1
ORDER BY quoted_fee_gbp DESC LIMIT 20;
