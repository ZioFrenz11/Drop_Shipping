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
