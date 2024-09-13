import requests
from config import PRINTFUL_API_KEY
from utils.api_utils import safe_api_call

def get_printful_most_popular():
    url = "https://api.printful.com/store/products"
    headers = {'Authorization': f'Bearer {PRINTFUL_API_KEY}'}
    response = safe_api_call(requests.get, url, headers=headers)
    products = response.json().get('result', [])
    if products:
        # Custom metric for Printful, assuming the first product is the most popular
        return products[0]
    return None
