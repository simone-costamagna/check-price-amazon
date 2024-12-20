from logging_config import configure_logging
from webdriver_manager import get_driver, close_driver
from price_checker import check_price
from email_handler import send_email
import config

if __name__ == "__main__":
    configure_logging()

    driver = get_driver()

    try:
        for product_link, product_price in config.PRODUCTS.items():
            success, message = check_price(driver, product_link, product_price)

            if success:
                send_email(
                    subject="Price Alert: Amazon Product",
                    content=message,
                )
    finally:
        close_driver(driver)