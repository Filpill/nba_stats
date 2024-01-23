#!/bin/bash
psql postgresql://root:root@pgdatabase:5432/nba -f tf/create_tf_season_averages.sql -f tf/create_tf_unioned_games.sql
