import requests
import os
import datetime as dt

ORIGIN_CODE = "MX"
API_KEY = os.environ.get("API_KEY_KIWI")


class FlightSearch:
    def __init__(self):
        self.endpoint_search = "https://api.tequila.kiwi.com/v2/search"
        self.endpoint_location = "https://api.tequila.kiwi.com/locations/query"
        self.authentication = {"apikey": API_KEY}
        self.code = None
        self.city = None
        self.outbound_date = None
        self.inbound_date = None
        self.stop_over = 0
        self.via_city = None
        self.price = None

    def get_code(self, city) -> str:
        parameters_code = {"term": city, "location_types": "city"}
        response = requests.get(url=self.endpoint_location, params=parameters_code, headers=self.authentication)
        response.raise_for_status()
        code = response.json()["locations"][0]["code"]
        return code

    def get_price(self, code) -> float:
        from_date = dt.datetime.now().today()
        to_date = from_date + dt.timedelta(weeks=24)
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        parameters_price = {
            "fly_from": ORIGIN_CODE,
            "fly_to": code,
            "date_from": from_date.strftime("%d/%m/%Y"),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 3,
            "nights_in_dst_to": 4,
            "curr": "MXN",
            "adult": 1,
            "max_stopovers": 0
        }

        response = requests.get(url=self.endpoint_search, params=parameters_price, headers=self.authentication)
        response.raise_for_status()
        try:
            data_payload = response.json()["data"][0]["price"]
            self.price = data_payload
            outbound = dt.datetime.strptime(response.json()["data"][0]["local_departure"], date_format).date()
            inbound = dt.datetime.strptime(response.json()["data"][-1]["route"][-1]["local_arrival"],
                                           date_format).date()
            self.outbound_date = outbound
            self.inbound_date = inbound

        except IndexError:
            try:
                parameters_price = {
                    "fly_from": ORIGIN_CODE,
                    "fly_to": code,
                    "date_from": from_date.strftime("%d/%m/%Y"),
                    "date_to": to_date.strftime("%d/%m/%Y"),
                    "nights_in_dst_from": 3,
                    "nights_in_dst_to": 4,
                    "curr": "MXN",
                    "max_stopovers": 2,
                    "adult": 1
                }

                response = requests.get(url=self.endpoint_search, params=parameters_price, headers=self.authentication)
                response.raise_for_status()
                data_payload = response.json()["data"][0]["price"]
                self.price = data_payload
                outbound = dt.datetime.strptime(response.json()["data"][0]["local_departure"], date_format).date()
                inbound = dt.datetime.strptime(response.json()["data"][-1]["route"][-1]["local_arrival"],
                                               date_format).date()
                self.outbound_date = outbound
                self.inbound_date = inbound
                self.stop_over = 2
                self.via_city = response.json()["data"][0]["route"][0]["cityTo"]
                return self.price

            except IndexError:
                self.price = 0
                return self.price

        else:
            return self.price



