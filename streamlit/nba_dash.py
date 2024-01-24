import psycopg2
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import date
from sqlalchemy import create_engine, Table
# @st.cache(allow_output_mutation=True)

# Connecting To Database
user = 'root'
password = 'root'
host = 'localhost'
port = '5432'
db = 'nba'
engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
engine.connect()

# Retrieve Data
query_1 = f"""
SELECT 
    player_name,
    season,
    points,
    rebounds,
    assists,
    blocks,
    steals,
    turnovers,
    personal_fouls,
    games_played,
    minutes_played
FROM tf_season_averages
WHERE 
    season = '2023'
ORDER BY points desc
LIMIT 15
;
"""

st.title('NBA Season Average Statistics')
df_data = pd.read_sql(query_1,con=engine)


# Table
st.text('Displaying NBA Data For Top Players')
st.table(df_data)

# Bar Chart
metric_select = st.selectbox(label = 'Metric Selection', options=['points','rebounds','assists','blocks','steals','turnovers','personal_fouls','games_played','minutes_played'])
df_bar_sorted = df_data.sort_values(by=metric_select, ascending=False)
chart_points = alt.Chart(df_bar_sorted).mark_bar().encode(
    x=alt.X('player_name', sort=None),
    y=metric_select
).properties(width = 700, height = 400, title = f'Most {metric_select} in Season')
st.write(chart_points)

# Player Percentage
query_2 = f"""
SELECT 
    player_name,
    season,
    points,
    field_goal_percentage,
    fg_3pt_percentage,
    free_throw_percentage
FROM tf_season_averages
WHERE 
    season = '2023'
ORDER BY points desc
LIMIT 15
;
"""
player_list = list(df_data['player_name'])
player_select = st.selectbox(label = 'Player Selection', options=player_list)

df_data_2 = pd.read_sql(query_2,con=engine)
def player_percentage(df_data_2,player_name):
    df_data_sub = df_data_2[['player_name','field_goal_percentage','fg_3pt_percentage','free_throw_percentage']]
    player_filter = df_data_sub['player_name'] == player_name
    player_index = df_data_sub[player_filter].index[0]
    df_player = df_data_sub[player_filter].T
    df_player = df_player[1::].reset_index() #Dropping Name
    df_player = df_player.rename(columns={"index": "attribute", player_index: "value"})
    return df_player

#Radar Plot

df_player = player_percentage(df_data_2,player_select)
fig = px.line_polar(df_player, r='value', theta='attribute',line_close=True)
fig.update_polars(radialaxis=dict(visible=True, range=[0,1]))
fig.update_traces(fill='toself')
fig.update_layout(title=f'{player_select} Shot Perentages')
st.plotly_chart(fig, use_container_width=True)