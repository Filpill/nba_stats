DO $$
BEGIN
	/*Dropping Table in Preparation for Replacing with Updated*/
	IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tf_unioned_games')
	THEN 
		DROP TABLE public.tf_unioned_games;
	END IF;
	
CREATE TABLE tf_unioned_games (
	game_id INT,
    game_date TIMESTAMP, 
	h_or_v TEXT,
	team_id INT, 
	team_name TEXT,
	score INT, 
	period INT, 
	postseason BOOL, 
	season INT, 
	status TEXT 
	);
	
WITH folded_games AS(
	SELECT
		id as game_id, 
		date as game_date, 
		'home' as h_or_v,
		home_team_id AS team_id, 
		home_team_score AS score, 
		period, 
		postseason, 
		season, 
		status 
	FROM public.games

	UNION ALL

	SELECT
		id as game_id, 
		date as game_date, 
		'visit' as h_or_v,
		visitor_team_id as team_id, 
		visitor_team_score as score,
		period, 
		postseason, 
		season, 
		status
	FROM public.games

	ORDER BY game_id
	)

INSERT INTO tf_unioned_games (
SELECT 
	game_id, 
	game_date, 
	h_or_v,
	team_id, 
	t.name as team_name,
	score,
	period, 
	postseason, 
	season, 
	status
FROM folded_games fg
INNER JOIN public.teams t ON t.id = fg.team_id
ORDER BY game_date desc
);
END $$;