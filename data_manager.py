import requests
import os

API_KEY_SHEETY = os.environ.get("API_KEY_SHEETY")
API_AUTH_SHEETY = os.environ.get("API_AUTH_SHEETY")


class DataManager:
    def __init__(self):
        self.api_key = API_KEY_SHEETY
        self.endpoint = f"https://api.sheety.co/{self.api_key}/flightDeals/"
        self.api_auth = API_AUTH_SHEETY
        self.authentication = {"Authorization": self.api_auth}
        self.data = []
        self.data_users = []

    def get_data(self):
        response = requests.get(url=f"{self.endpoint}/prices")
        response.raise_for_status()
        data = response.json()["prices"]
        for record in data:
            if "code" not in record:
                record = {
                    "city": record["city"],
                    "code": "",
                    "lowerPrice": record["lowestPrice"],
                    "id": record["id"]
                }
                self.data.append(record)
            else:
                self.data.append(record)

        return self.data

    def update_information(self, record, json_data):
        response = requests.put(url=f"{self.endpoint}/prices/{record}", json=json_data)

    def get_emails(self):
        response = requests.get(url=f"{self.endpoint}/users")
        response.raise_for_status()
        data = response.json()["users"]
        for record in data:
            email = record["email"]
            self.data_users.append(email)
        return self.data_users


