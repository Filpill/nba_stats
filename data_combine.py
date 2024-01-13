import os
import sys
import json

def combine_json(endpoint):
    print(f'Consolidating raw {endpoint} JSON files')
    json_combined = []
    folder = os.path.join(sys.path[0],'data','raw',f'{endpoint}')
    for f in os.listdir(folder):
         with open(os.path.join(folder,f), 'r') as f:
            json_combined.append(json.load(f))
    json_combined = [item for json_f in json_combined for item in json_f] #Flatten

    combined_filepath = os.path.join(sys.path[0],'data','combined',f'{endpoint}.json')
    with open(combined_filepath, 'w') as f:
       json.dump(json_combined,f,indent=4)

endpoints = {
    1 : "players",
    2 : "teams",
    3 : "games",
    4 : "season_averages"
}

for key in endpoints:
    combine_json(endpoints.get(key))