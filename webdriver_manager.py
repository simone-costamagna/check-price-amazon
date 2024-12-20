import logging
from selenium import webdriver

def get_driver() -> webdriver.Chrome:
    """
    Get a configured Chrome WebDriver instance.
    :return: Configured WebDriver instance for Chrome.
    """
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_driver = webdriver.Chrome(options=chrome_options)
        logging.info("WebDriver initialized successfully.")
        return chrome_driver
    except Exception as ex:
        logging.error(f"Failed to initialize WebDriver: {ex}")
        raise

def close_driver(driver: webdriver.Chrome):
    """
    Close the WebDriver instance.
    :param driver: The WebDriver instance to close.
    """
    try:
        driver.quit()
        logging.info("WebDriver closed successfully.")
    except Exception as ex:
        logging.warning(f"Error while closing WebDriver: {ex}")