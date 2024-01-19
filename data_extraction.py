import os
import sys
import json
import pandas as pd
from time import sleep
from shared.functions import apiRequest

def endpoint_pages(endpoint):
    print(f'Retrieving NBA Data For {endpoint}')
    base_url = 'https://www.balldontlie.io/api/v1'
    per_page = 100
    total_pages = apiRequest(f'{base_url}/{endpoint}?per_page={per_page}').get('meta').get('total_pages')

    for i in range(1,total_pages):
        page_of_data = apiRequest(f'{base_url}/{endpoint}?page={i}?&per_page={per_page}')
        filepath = os.path.join(sys.path[0],'docker_sql','data','raw',f'{endpoint}',f'page_{i}.json')
        with open(filepath, 'w') as f:
            json.dump(page_of_data.get('data'),f, indent=4)

def season_pages(season):
    print(f'Retrieving NBA Data For {season} - Season Averages')
    player_path = os.path.join(sys.path[0],'docker_sql','data','combined','players.json')
    df_players = pd.read_json(player_path).sort_values('id')
    player_list = list(df_players['id'])
    player_list = [str(id) for id in player_list]
    request_interval = 100
    season_avg_req_intervals = [player_list[i:i+request_interval] for i in range(0, len(player_list),request_interval)] #Limited request processing for players
    season_avg_req_intervals = {index: sublist for index, sublist in enumerate(season_avg_req_intervals)}

    for key in season_avg_req_intervals:
        print("Request Sub-Array: ", key)
        base_url = f'https://www.balldontlie.io/api/v1/season_averages?season={season}'
        filepath = os.path.join(sys.path[0],'docker_sql','data','raw',f'season_averages',f'{season}_page_{key}.json')
        for id in season_avg_req_intervals.get(key):
            base_url = base_url + f"&player_ids[]={id}"
        page_of_data = apiRequest(base_url)
        sleep(3) # Rate limit is currently 60/minute
        with open(filepath, 'w') as f:
            json.dump(page_of_data.get('data'),f, indent=4)

def main():
    endpoints = {
        1 : "players",
        2 : "teams",
        3 : "games",
    }

    # For standard endpoints
    # for endpoint in endpoints.values():
        # endpoint_pages(endpoints.get(endpoint))

    # Extract Yearly Season Averages
    season_list = range(1990,1996,1)
    for season in season_list:
        season_pages(season)

if __name__ == "__main__":
    main()