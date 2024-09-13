'''

This file handles environment variables and API keys.

'''


import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API keys and other configurations
SHOPIFY_API_KEY = os.getenv('SHOPIFY_API_KEY')
SHOPIFY_PASSWORD = os.getenv('SHOPIFY_PASSWORD')
SHOPIFY_STORE_NAME = os.getenv('SHOPIFY_STORE_NAME')

WOOCOMMERCE_API_KEY = os.getenv('WOOCOMMERCE_API_KEY')
WOOCOMMERCE_SECRET = os.getenv('WOOCOMMERCE_SECRET')
WOOCOMMERCE_STORE_URL = os.getenv('WOOCOMMERCE_STORE_URL')

PRINTIFY_API_KEY = os.getenv('PRINTIFY_API_KEY')
PRINTFUL_API_KEY = os.getenv('PRINTFUL_API_KEY')
TEESPRING_API_KEY = os.getenv('TEESPRING_API_KEY')
MODALYST_API_KEY = os.getenv('MODALYST_API_KEY')
ALIEXPRESS_RAPIDAPI_KEY = os.getenv('ALIEXPRESS_RAPIDAPI_KEY')
SHIPSTATION_API_KEY = os.getenv('SHIPSTATION_API_KEY')
