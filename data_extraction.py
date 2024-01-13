import os
import sys
import json
import pandas as pd
from shared.functions import apiRequest

def endpoint_pages(endpoint):
    print(f'Retrieving NBA Data For {endpoint}')
    base_url = 'https://www.balldontlie.io/api/v1'
    per_page = 100
    total_pages = apiRequest(f'{base_url}/{endpoint}?per_page={per_page}').get('meta').get('total_pages')

    for i in range(1,total_pages):
        page_of_data = apiRequest(f'{base_url}/{endpoint}?page={i}?&per_page={per_page}')
        filepath = os.path.join(sys.path[0],'data','raw',f'{endpoint}',f'page_{i}.json')
        with open(filepath, 'w') as f:
            json.dump(page_of_data.get('data'),f, indent=4)

def season_pages(season):
    print(f'Retrieving NBA Data For {season} - Season Averages')
    df_players = pd.read_json('players_full_list.json').sort_values('id')
    player_list = list(df_players['id'])
    player_list = [str(id) for id in player_list]
    request_interval = 100
    season_avg_req_intervals = [player_list[i:i+request_interval] for i in range(0, len(player_list),request_interval)] #Limited request processing for players
    season_avg_req_intervals = {index: sublist for index, sublist in enumerate(season_avg_req_intervals)}

    for key in season_avg_req_intervals:
        print("Request Sub-Array: ", key)
        base_url = f'https://www.balldontlie.io/api/v1/season_averages?season={season}'
        filepath = os.path.join(sys.path[0],'data','raw',f'season_averages_json',f'{2023}_page_{key}.json')
        for id in season_avg_req_intervals.get(key):
            base_url = base_url + f"&player_ids[]={id}"
        page_of_data = apiRequest(base_url)
        with open(filepath, 'w') as f:
            json.dump(page_of_data.get('data'),f, indent=4)


endpoints = {
    1 : "players",
    2 : "teams",
    # 3 : "games",
    4 : "season_averages"
}

print(endpoints)
end_select = int(input("Select Endpoint Data to Retrieve: "))
endpoint_pages(endpoints.get(end_select))