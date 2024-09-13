import requests
from config import PRINTIFY_API_KEY
from utils.api_utils import safe_api_call

def get_printify_most_popular():
    url = "https://api.printify.com/v1/catalog/products.json"
    headers = {'Authorization': f'Bearer {PRINTIFY_API_KEY}'}
    response = safe_api_call(requests.get, url, headers=headers)
    products = response.json()
    most_popular_product = max(products, key=lambda x: x.get('popularity_metric', 0))
    return most_popular_product