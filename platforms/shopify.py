import requests
import logging
from config import SHOPIFY_API_KEY, SHOPIFY_PASSWORD, SHOPIFY_STORE_NAME
from utils.api_utils import safe_api_call

def insert_product_shopify(product_data):
    url = f"https://{SHOPIFY_STORE_NAME}.myshopify.com/admin/api/2023-04/products.json"
    headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': SHOPIFY_PASSWORD}
    response = safe_api_call(requests.post, url, headers=headers, json=product_data)
    logging.info(f"Shopify listing response: {response.json()}")
