import config
import os
from dotenv import load_dotenv
import logging
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

load_dotenv()

# Constants for environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN")

if not EMAIL_ADDRESS or not GMAIL_TOKEN:
    raise EnvironmentError("Missing required environment variables: EMAIL_ADDRESS and/or GMAIL_TOKEN")


def configure_logging():
    """
    Set up logging configuration defining log format, level, and output.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler()]
    )


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


def check_price(driver: webdriver.Chrome, link: str, established_price: float) -> tuple[bool, str]:
    """
    Check the price of a product and determine if it is below the established price.

    :param driver: The WebDriver instance.
    :param link: Product link.
    :param established_price: Price threshold.
    :return: Tuple containing a success flag and a message.
    """
    logging.info(f"Checking price for {link}...")

    try:
        driver.implicitly_wait(30)
        driver.get(link)

        # Attempt to locate price elements
        try:
            price_section = driver.find_element("xpath", '(//div[@class="a-section a-spacing-none aok-align-center aok-relative"])[1]')
            price_span = price_section.find_element("xpath", './/span[contains(@class, "a-price")]')
            price_whole = price_span.find_element("xpath", './span[2]/span[1]').text
            price_fraction = price_span.find_element("xpath", './span[2]/span[2]').text
        except NoSuchElementException:
            logging.warning(f"Price elements not found for link: {link}")
            return False, ""

        # Calculate the total price
        price = float(price_whole.replace(",", "")) + float(price_fraction) / 100

        if price <= established_price:
            logging.info(f"Price for {link} is below threshold: {price}")
            return True, f"Product: {link}\nThreshold: {established_price}\nCurrent price: {price:.2f}"

        logging.info(f"Price for {link} is above threshold: {price}")
    except Exception as ex:
        logging.error(f"Error checking price for {link}: {ex}")

    return False, ""


def send_email(recipient: str, subject: str, content: str):
    """
    Send an email with the specified subject and content to the given recipient.

    :param recipient: Recipient's email address.
    :param subject: Email subject.
    :param content: Email body content.
    """
    logging.info("Sending email...")

    try:
        message = MIMEText(content, _charset="utf-8")
        message["Subject"] = subject
        message["From"] = EMAIL_ADDRESS
        message["To"] = recipient

        with smtplib.SMTP("smtp.gmail.com", 587) as email:
            email.ehlo()
            email.starttls()
            email.login(EMAIL_ADDRESS, GMAIL_TOKEN)
            email.sendmail(EMAIL_ADDRESS, recipient, message.as_string())

        logging.info("Email sent successfully.")
    except Exception as ex:
        logging.error(f"Failed to send email: {ex}")


if __name__ == "__main__":
    configure_logging()

    driver = get_driver()

    try:
        for product_link, product_price in config.PRODUCTS.items():
            success, message = check_price(driver, product_link, product_price)

            if success:
                send_email(EMAIL_ADDRESS, "Price Alert: Amazon Product", message)
    finally:
        close_driver(driver)
