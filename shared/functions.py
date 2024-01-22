import json
import requests

def apiRequest(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    if response.status_code != 200:
        print(f'{response.status_code} - {response.reason}')
        KeyboardInterrupt

def is_json_empty(json_file):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
            return not bool(data)
    except (json.JSONDecodeError):
        return True