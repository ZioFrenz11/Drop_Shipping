'''
This file will handle the high-level logic, integrating the suppliers, platforms, and utility modules.
'''

import logging
from suppliers.aliexpress import get_aliexpress_top_sellers
from suppliers.printify import get_printify_most_popular
from platforms.shopify import insert_product_shopify
from platforms.woocommerce import insert_product_woocommerce
from utils.stock_check import check_stock
from utils.profit_calc import calculate_profit
from utils.api_utils import get_shipping_cost
from utils.crm import send_email_notification
from utils.logger import setup_logging

# Initialize logging
setup_logging()


def main():
    logging.info("Starting the drop-shipping automation process.")

    # Fetch products from suppliers
    aliexpress_item = get_aliexpress_top_sellers()
    printify_product = get_printify_most_popular()

    # Check stock, calculate profit, and insert products
    if aliexpress_item and check_stock(aliexpress_item):
        shipping_cost = get_shipping_cost(aliexpress_item)
        if calculate_profit(aliexpress_item, shipping_cost):
            insert_product_shopify(aliexpress_item)
            insert_product_woocommerce(aliexpress_item)
            send_email_notification(f"Product {aliexpress_item['title']} has been listed!")

    if printify_product and check_stock(printify_product):
        shipping_cost = get_shipping_cost(printify_product)
        if calculate_profit(printify_product, shipping_cost):
            insert_product_shopify(printify_product)
            insert_product_woocommerce(printify_product)
            send_email_notification(f"Product {printify_product['title']} has been listed!")


if __name__ == "__main__":
    main()

import requests
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt
import os
import json

# Load environment variables
load_dotenv()

# API keys and configurations
shopify_api_key = os.getenv('SHOPIFY_API_KEY')
shopify_password = os.getenv('SHOPIFY_PASSWORD')
shopify_store_name = os.getenv('SHOPIFY_STORE_NAME')

woocommerce_api_key = os.getenv('WOOCOMMERCE_API_KEY')
woocommerce_secret = os.getenv('WOOCOMMERCE_SECRET')
woocommerce_store_url = os.getenv('WOOCOMMERCE_STORE_URL')

printify_api_key = os.getenv('PRINTIFY_API_KEY')
printful_api_key = os.getenv('PRINTFUL_API_KEY')
teespring_api_key = os.getenv('TEESPRING_API_KEY')
modalyst_api_key = os.getenv('MODALYST_API_KEY')
aliexpress_rapidapi_key = os.getenv('ALIEXPRESS_RAPIDAPI_KEY')
shipstation_api_key = os.getenv('SHIPSTATION_API_KEY')

email_sender = os.getenv('EMAIL_SENDER')
email_password = os.getenv('EMAIL_PASSWORD')
email_recipient = os.getenv('EMAIL_RECIPIENT')

# Set up logging
logging.basicConfig(filename='dropshipping_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Email notification function
def send_email(subject, body):
    """Send an email to notify about important events."""
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        server.quit()
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

# Retry decorator for API calls
@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def safe_api_call(func, *args, **kwargs):
    """Attempt to call an API with retrying and logging."""
    try:
        response = func(*args, **kwargs)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response
    except Exception as e:
        logging.error(f"API call failed: {e}")
        raise

# Advanced Product Sourcing Functions (AliExpress, Printify, Printful, etc.)
def get_aliexpress_top_sellers(api_key, category_id):
    """Fetch the most sold item from AliExpress based on category."""
    url = "https://aliexpress-datahub.p.rapidapi.com/item_search"
    headers = {'X-RapidAPI-Key': api_key, 'X-RapidAPI-Host': 'aliexpress-datahub.p.rapidapi.com'}
    params = {'category_id': category_id, 'sort': 'orders'}
    response = safe_api_call(requests.get, url, headers=headers, params=params)
    top_items = response.json().get('data', {}).get('products', [])
    if top_items:
        send_email("New Top Product Found", f"Found a top product on AliExpress: {top_items[0]['title']}")
        return top_items[0]  # Return the most sold item
    return None

def get_printify_most_popular(api_key):
    """Fetch the most popular product from Printify."""
    url = "https://api.printify.com/v1/catalog/products.json"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = safe_api_call(requests.get, url, headers=headers)
    products = response.json()
    most_popular_product = max(products, key=lambda x: x.get('popularity_metric', 0))
    send_email("New Popular Printify Product Found", f"Found a popular product on Printify: {most_popular_product['title']}")
    return most_popular_product

# Repeat similar functions for Printful, TeeSpring, Modalyst...

# Stock Checking: Ensure products are available before listing
def check_stock(product):
    """Check if the product is in stock."""
    return product.get('stock', 0) > 0

# Dynamic Pricing Model: Price Monitoring, Shipping, and Profit Calculation
def calculate_price(product, shipping_cost, profit_margin=0.2):
    """Calculate the price of the product with a dynamic pricing model."""
    base_price = float(product.get('price', 0))
    total_cost = base_price + shipping_cost
    return total_cost * (1 + profit_margin)

# Shipping Calculation: Fetch real-time shipping rates via ShipStation
def get_shipping_cost(product):
    """Calculate shipping cost via ShipStation or other shipping services."""
    url = f"https://ssapi.shipstation.com/rates"
    # Example rate request payload
    payload = {
        "carrierCode": "stamps_com",
        "serviceCode": "usps_first_class_mail",
        "packageCode": "package",
        "fromPostalCode": "94103",
        "toPostalCode": product.get('postal_code', '10001'),
        "weight": {"value": 16, "units": "ounces"},
        "dimensions": {"units": "inches", "length": 10, "width": 5, "height": 5}
    }
    headers = {'Authorization': f'Bearer {shipstation_api_key}'}
    response = safe_api_call(requests.post, url, headers=headers, json=payload)
    return response.json().get('rate', 0)

# Profit Calculation: Automatically computes profit margins
def calculate_profit(product, shipping_cost):
    """Compute profit margin and filter out non-profitable products."""
    sale_price = calculate_price(product, shipping_cost)
    base_price = float(product.get('price', 0))
    profit = sale_price - (base_price + shipping_cost)
    return profit > 0

# Fallback logic for multi-supplier product availability
def find_product_across_suppliers(product_name):
    """Try to find the product across multiple suppliers."""
    suppliers = [get_aliexpress_top_sellers, get_printify_most_popular]  # Add more supplier functions here
    for supplier in suppliers:
        product = supplier(aliexpress_rapidapi_key)  # Pass correct API key
        if product and check_stock(product):
            return product
    return None

# Multi-platform insertion (Shopify, WooCommerce)
def create_shopify_product(api_key, password, store_name, product_data):
    """Create a product listing on Shopify."""
    url = f"https://{store_name}.myshopify.com/admin/api/2023-04/products.json"
    headers = {'Content-Type': 'application/json', 'X-Shopify-Access-Token': password}
    response = safe_api_call(requests.post, url, headers=headers, json=product_data)
    send_email("New Product Listed on Shopify", f"Product '{product_data['product']['title']}' listed on Shopify")
    return response.json()

def create_woocommerce_product(api_key, secret, store_url, product_data):
    """Create a product listing on WooCommerce."""
    url = f"{store_url}/wp-json/wc/v3/products"
    auth = (api_key, secret)
    response = safe_api_call(requests.post, url, json=product_data, auth=auth)
    send_email("New Product Listed on WooCommerce", f"Product '{product_data['title']}' listed on WooCommerce")
    return response.json()

# Product data extraction for platform integration
def extract_product_info(product):
    """Convert product data into the required format for Shopify and WooCommerce."""
    return {
        "product": {
            "title": product.get('title'),
            "body_html": product.get('description', ''),
            "vendor": "Your Store Name",
            "product_type": "clothing",
            "variants": [
                {
                    "option1": "Default Title",
                    "price": calculate_price(product, get_shipping_cost(product)),
                    "sku": product.get('sku'),
                    "inventory_quantity": product.get('stock', 0),
                }
            ]
        }
    }

# Insert product into multiple platforms (Shopify, WooCommerce)
def insert_product_to_platforms(product_data):
    """Insert the product data into Shopify and WooCommerce."""
    try:
        # Insert to Shopify
        create_shopify_product(shopify_api_key, shopify_password, shopify_store_name, product_data)
        # Insert to WooCommerce
        create_woocommerce_product(woocommerce_api_key, woocommerce_secret, woocommerce_store_url, product_data)
        logging.info(f"Product '{product_data['product']['title']}' successfully listed on both platforms.")
    except Exception as e:
        logging.error(f"Failed to list product on platforms: {e}")

# Example Usage: Fetch most sold items, check stock, calculate profit, and insert into platforms
def main():
    logging.info("Starting the drop-shipping automation process.")
    aliexpress_item = get_aliexpress_top_sellers(aliexpress_rapidapi_key, '100005434')
    printify_product = get_printify_most_popular(printify_api_key)
    
    if aliexpress_item and check_stock(aliexpress_item):
        shipping_cost = get_shipping_cost(aliexpress_item)
        if calculate_profit(aliexpress_item, shipping_cost):
            product_data = extract_product_info(aliexpress_item)
            insert_product_to_platforms(product_data)
    
    if printify_product and check_stock(printify_product):
        shipping_cost = get_shipping_cost(printify_product)
        if calculate_profit(printify_product, shipping_cost):
            product_data = extract_product_info(printify_product)
            insert_product_to_platforms(product_data)

if __name__ == "__main__":
    main()
