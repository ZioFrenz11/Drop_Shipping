import requests
import logging
from config import WOOCOMMERCE_API_KEY, WOOCOMMERCE_SECRET, WOOCOMMERCE_STORE_URL
from utils.api_utils import safe_api_call

def insert_product_woocommerce(product_data):
    url = f"{WOOCOMMERCE_STORE_URL}/wp-json/wc/v3/products"
    auth = (WOOCOMMERCE_API_KEY, WOOCOMMERCE_SECRET)
    response = safe_api_call(requests.post, url, json=product_data, auth=auth)
    logging.info(f"WooCommerce listing response: {response.json()}")
