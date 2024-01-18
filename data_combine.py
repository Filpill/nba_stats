import os
import sys
import json
import pandas as pd

def combine_json(endpoint):
    print(f'Consolidating raw {endpoint} JSON files')
    json_combined = []
    folder = os.path.join(sys.path[0],'docker_sql','data','raw',f'{endpoint}')
    for f in os.listdir(folder):
        json_path = os.path.join(folder,f)
        if is_json_empty(json_path) == False:
            with open(json_path, 'r') as f:
                json_combined.append(json.load(f))
    json_combined = [item for json_f in json_combined for item in json_f] #Flatten

    combined_filepath = os.path.join(sys.path[0],'docker_sql','data','combined',f'{endpoint}.json')
    with open(combined_filepath, 'w') as f:
       json.dump(json_combined,f,indent=4)

def replace_team_id(df,col_name):
    team_json = list(df[col_name])
    team_id = [row.get('id') for row in team_json]
    df[col_name] = team_id
    df.rename(columns={col_name:f'{col_name}_id'},inplace=True)
    print(f'replaced {col_name} list of dict with list of id\'s')
    return df

def is_json_empty(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return not bool(data)
    except (json.JSONDecodeError):
        return True

def main():
    endpoints = {
        1 : "players",
        2 : "teams",
        3 : "games",
        4 : "season_averages"
    }

    # folder = os.path.join(sys.path[0],'docker_sql','data','raw','season_averages')
    # for file in os.listdir(folder):
    #     fp = os.path.join(folder,file)
    #     print(file,is_json_empty(fp))

    for key in endpoints:
       combine_json(endpoints.get(key))

    # Fixing Team ID Cols For Games
    games_file = os.path.join(sys.path[0],'docker_sql','data','combined',f'games.json')
    df_games = pd.read_json(games_file)
    for team in ['home_team','visitor_team']:
    # If dict column in table, replace with team id
       if team in df_games.columns:
           df_games = replace_team_id(df_games,team)   
    df_games.to_json(games_file)

if __name__ == "__main__":
    main()