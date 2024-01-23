DO $$
BEGIN
	/*Dropping Table in Preparation for Replacing with Updated*/
	IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tf_season_averages')
	THEN 
		DROP TABLE public.tf_season_averages;
	END IF;

CREATE TABLE tf_season_averages AS (
SELECT 
    min AS minutes_played,
    fgm AS fg_made,
    fga AS fg_attempted,
    fg3m AS fg_3pt_made,
    fg3a AS fg_3pt_attempted,
    ftm AS free_throws_made,
    fta AS free_throws_attempted,
    oreb AS offensive_rebounds,
    dreb AS defensive_rebounds,
    reb AS rebounds,
    ast AS assists,
    turnover AS turnovers,
    stl AS steals,
    blk AS blocks,
    pf AS personal_fouls,
    pts AS points,
    fg_pct AS field_goal_percentage,
    fg3_pct AS fg_3pt_percentage,
    ft_pct AS free_throw_percentage
FROM public.season_averages
);
END $$;