import requests

def apiRequest(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    if response.status_code != 200:
        print(f'{response.status_code} - {response.reason}')
        KeyboardInterrupt