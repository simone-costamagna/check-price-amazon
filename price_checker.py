import logging
from selenium.common.exceptions import NoSuchElementException

def check_price(driver, link: str, established_price: float) -> tuple[bool, str]:
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

        try:
            price_section = driver.find_element("xpath", '(//div[@class="a-section a-spacing-none aok-align-center aok-relative"])[1]')
            price_span = price_section.find_element("xpath", './/span[contains(@class, "a-price")]')
            price_whole = price_span.find_element("xpath", './span[2]/span[1]').text
            price_fraction = price_span.find_element("xpath", './span[2]/span[2]').text
        except NoSuchElementException:
            logging.warning(f"Price elements not found for link: {link}")
            return False, ""

        price = float(price_whole.replace(",", "")) + float(price_fraction) / 100

        if price <= established_price:
            logging.info(f"Price {price} for {link} is below threshold {established_price}")
            return True, f"Product: {link}\nThreshold: {established_price}\nCurrent price: {price:.2f}"

        logging.info(f"Price {price} for {link} is above threshold {established_price}")
    except Exception as ex:
        logging.error(f"Error checking price for {link}: {ex}")

    return False, ""