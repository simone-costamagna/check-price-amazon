import logging
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
GMAIL_TOKEN = os.getenv("GMAIL_TOKEN")

if not EMAIL_ADDRESS or not GMAIL_TOKEN:
    raise EnvironmentError("Missing required environment variables: EMAIL_ADDRESS and/or GMAIL_TOKEN")

def send_email(subject: str, content: str):
    """
    Send an email with the specified subject and content to the given recipient.
    :param subject: Email subject.
    :param content: Email body content.
    """
    logging.info("Sending email...")

    try:
        message = MIMEText(content, _charset="utf-8")
        message["Subject"] = subject
        message["From"] = EMAIL_ADDRESS
        message["To"] = EMAIL_ADDRESS

        with smtplib.SMTP("smtp.gmail.com", 587) as email:
            email.ehlo()
            email.starttls()
            email.login(EMAIL_ADDRESS, GMAIL_TOKEN)
            email.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message.as_string())

        logging.info("Email sent successfully.")
    except Exception as ex:
        logging.error(f"Failed to send email: {ex}")