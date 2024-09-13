import requests
from config import MODALYST_API_KEY
from utils.api_utils import safe_api_call

def get_modalyst_most_popular():
    url = "https://api.modalyst.co/v1/products"
    headers = {'Authorization': f'Bearer {MODALYST_API_KEY}'}
    params = {'sort': 'trending'}  # Assuming 'trending' indicates popular
    response = safe_api_call(requests.get, url, headers=headers, params=params)
    products = response.json().get('products', [])
    if products:
        return products[0]  # Return most popular product
    return None
