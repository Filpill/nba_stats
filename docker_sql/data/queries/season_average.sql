SELECT 
	p.first_name,
	p.last_name, 
	season, 
	games_played, 
	min as minutes_played, 
	fgm as fg_made, 
	fga as fg_attempted, 
	fg3m as fg_3pt_made, 
	fg3a as fg_3pt_attempted, 
	ftm as free_throws_made, 
	fta as free_throws_attempted, 
	oreb as offensive_rebounds, 
	dreb as defensive_rebounds, 
	reb as rebounds, 
	ast as assists, 
	stl as steals, 
	blk as blocks, 
	turnover, 
	pf as personal_fouls, 
	pts as points, 
	fg_pct as field_goal_percentage, 
	fg3_pct as fg_3pt_percentage, 
	ft_pct as free_throw_percentage
FROM public.season_averages sa
INNER JOIN public.players p ON sa.player_id = p.id
-- WHERE 
-- 	lower(first_name) = 'michael'
-- 	AND
-- 	lower(last_name) = 'jordan'
	