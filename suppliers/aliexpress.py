import requests
from config import ALIEXPRESS_RAPIDAPI_KEY
from utils.api_utils import safe_api_call

def get_aliexpress_top_sellers(category_id='100005434'):
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search"
    headers = {
        'X-RapidAPI-Key': ALIEXPRESS_RAPIDAPI_KEY,
        'X-RapidAPI-Host': 'aliexpress-datahub.p.rapidapi.com'
    }
    params = {'category_id': category_id, 'sort': 'orders'}
    response = safe_api_call(requests.get, url, headers=headers, params=params)
    return response.json().get('data', {}).get('products', [])[0]
