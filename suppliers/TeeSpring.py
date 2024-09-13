import requests
from config import TEESPRING_API_KEY
from utils.api_utils import safe_api_call

def get_teespring_most_popular():
    url = "https://api.teespring.com/v1/products"
    headers = {'Authorization': f'Bearer {TEESPRING_API_KEY}'}
    params = {'sort': 'popularity'}  # Sort by popularity
    response = safe_api_call(requests.get, url, headers=headers, params=params)
    products = response.json().get('products', [])
    if products:
        return products[0]
    return None
