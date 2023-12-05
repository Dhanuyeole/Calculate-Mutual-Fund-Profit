import requests

def get_mf_data(scheme_code):
    api_url = f'https://api.mfapi.in/mf/{scheme_code}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
