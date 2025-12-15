import requests
import pandas as pd
import json
def news(symbol):
    api_key = 'avfv2Nm9G79Man278Q9Z7SzB8Lr9YBUAuENi91L7'
    url = 'https://api.marketaux.com/v1/news/all'
    params = {
        'api_token': api_key,
        'limit': 10,
        'symbols': symbol,
        'language': 'en',
        'filter_entities': 'true'
    }
    response = requests.get(url, params)
    data = response.json()
    df = pd.DataFrame(data['data'])
    df.to_csv('marketaux.csv')
    return df