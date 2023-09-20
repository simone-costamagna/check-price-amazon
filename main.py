import os
from config import *
import smtplib
from email.mime.text import MIMEText


def send_email(address: str, subject: str, content: str):
    """
    An email is generated and sent when provided with an email address, subject, and content

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
    send_email(EMAIL_ADDRESS, "Update from check-price-amazon", "Testing")
