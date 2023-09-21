import os
from config import *
import smtplib
from email.mime.text import MIMEText

from selenium import webdriver


class GetDriverException(Exception):
    pass


def get_driver() -> webdriver.chrome.webdriver.WebDriver:
    """
    get the web browsing driver.

    :return chrome_driver: driver for web browsing
    """

    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_driver = webdriver.Chrome(options=chrome_options)
    except Exception as ex:
        raise GetDriverException('Cannot get the driver from Chrome.', str(ex))

    return chrome_driver


class CheckPrice(Exception):
    pass


def check_price(driver: webdriver.chrome.webdriver.WebDriver, link: str, established_price: float) -> str:
    """
    Verify the cost of an item and determine whether it falls below the established price.

    :param driver: driver for web browsing
    :param link: product link
    :param established_price: established price
    :return: content of the email with the price information if the outcome is positive otherwise None
    """

    driver.implicitly_wait(30)
    driver.get(link)

    try:
        xpath_expression = '//div[@id="apex_desktop_qualifiedBuybox"]/div[3]/div[1]/span[2]/span[2]/span[1]'
        span_price_euros = driver.find_element("xpath", xpath_expression)
        price_euros_string = span_price_euros.text

        xpath_expression = '//div[@id="apex_desktop_qualifiedBuybox"]/div[3]/div[1]/span[2]/span[2]/span[2]'
        span_price_cents = driver.find_element("xpath", xpath_expression)
        price_cents_string = span_price_cents.text

        euros = float(price_euros_string)
        cents = float(price_cents_string) / 100

        price = euros + cents
    except Exception as ex:
        raise CheckPrice(f"Impossibly read the price.", str(ex))

    if price <= established_price:
        return f"Product: {link}\nEstablished price: {established_price}\nCurrent price: {price}"
    else:
        return None


def send_email(address: str, subject: str, content: str):
    """
    An email is generated and sent when provided with an email address, subject, and content.

    :param address: recipient's email address
    :param subject: subject of the email
    :param content: content of the email
    :return: None
    """

    # Obtain the security token to access the email inbox
    GMAIL_TOKEN = os.environ["GMAIL_TOKEN"]

    message = MIMEText(content, _charset="utf-8")
    message["Subject"] = subject

    email = smtplib.SMTP("smtp.gmail.com", 587)
    email.ehlo()
    email.starttls()
    email.login("scostamagna.momo@gmail.com", GMAIL_TOKEN)

    email.sendmail("scostamagna.momo@gmail.com", address, message.as_string())

    email.quit()


if __name__ == "__main__":
    driver = get_driver()
    for product_link, product_price in PRODUCTS.items():
        response = check_price(driver, product_link, product_price)

        if response is not None:
            send_email(EMAIL_ADDRESS, "Update from check-price-amazon", response)

    driver.quit()
