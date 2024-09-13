import requests
import logging
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(5))
def safe_api_call(func, *args, **kwargs):
    """
    A safe wrapper around API calls with retry logic.
    """
    try:
        response = func(*args, **kwargs)
        response.raise_for_status()  # Raise exception for bad responses
        return response
    except Exception as e:
        logging.error(f"API call failed: {e}")
        raise

def get_shipping_cost(product):
    """
    Simulate the fetching of real-time shipping cost.
    For now, return a dummy value.
    """
    return 5.00  # Dummy shipping cost for now
