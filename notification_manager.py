import os
import smtplib
from twilio.rest import Client


TW_SID = os.environ.get("API_TW_SID")
TW_AUTH = os.environ.get("API_TW_AUTH")
USERNAME = os.environ.get("EMAIL_USERNAME")
PASSWORD = os.environ.get("EMAIL_PASSWORD")
TW_PHONE_NUMBER = os.environ.get("TW_PHONE_NUMBER")
PERS_PHONE_NUMBER = os.environ.get("PERS_PHONE_NUMBER")

class NotificationManager:
    def __init__(self):
        self.client = Client(TW_SID, TW_AUTH)

    # def send_message(self, msg):
    #     message = self.client.messages.create(
    #         body=msg,
    #         from_=TW_PHONE_NUMBER,
    #         to=PERS_PHONE_NUMBER
    #     )
    #
    #     print(message.sid)

    def send_emails(self, email, message):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=USERNAME, password=PASSWORD)
            connection.sendmail(from_addr=USERNAME,
                                to_addrs=email,
                                msg=message)



