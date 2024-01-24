DO $$
BEGIN
        /*Dropping Table in Preparation for Replacing with Updated*/
        IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'tf_season_averages')
        THEN
                DROP TABLE public.tf_season_averages;
        END IF;

CREATE TABLE tf_season_averages AS (
SELECT
    t.player_id,
    p.first_name || ' ' || p.last_name AS player_name,
	t.season,
    t.games_played,
    SPLIT_PART(t.min,':', 1)::float + ((SPLIT_PART(t.min,':', 2)::float)/60) AS minutes_played,
    t.fgm AS fg_made,
    t.fga AS fg_attempted,
    t.fg3m AS fg_3pt_made,
    t.fg3a AS fg_3pt_attempted,
    t.ftm AS free_throws_made,
    t.fta AS free_throws_attempted,
    t.oreb AS offensive_rebounds,
    t.dreb AS defensive_rebounds,
    t.reb AS rebounds,
    t.ast AS assists,
    t.turnover AS turnovers,
    t.stl AS steals,
    t.blk AS blocks,
    t.pf AS personal_fouls,
    t.pts AS points,
    t.fg_pct AS field_goal_percentage,
    t.fg3_pct AS fg_3pt_percentage,
    t.ft_pct AS free_throw_percentage
FROM public.season_averages t
INNER JOIN public.players p ON t.player_id = p.id
);
END $$;
