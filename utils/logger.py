import logging

def setup_logging():
    """
    Set up logging for the entire application.
    Logs will be written to dropshipping_app.log.
    """
    logging.basicConfig(filename='dropshipping_app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
