from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()
# --------------------------------------------- Application Routes --------------------------------------------------- #
all_data = data_manager.get_data()

for record in all_data:
    if record["code"] == "":
        code = flight_search.get_code(record["city"])
        json_code = {"price": {"code": code}}
        record["code"] = code
        data_manager.update_information(record=int(record["id"]), json_data=json_code)

emails = data_manager.get_emails()

for record in data_manager.data:
    price = flight_search.get_price(record["code"])
    connection = flight_search.stop_over
    if price == 0:
        continue

    elif price < record["lowestPrice"]:
        if connection == 0:
            json_price = {"price": {"lowestPrice": round(price, 2)}}
            data_manager.update_information(record=int(record["id"]), json_data=json_price)
            record["price"] = price
            msg0 = "Subject: Flight Deal!\n\n"
            msg1 = f"Low Price Alert! Only {round(flight_search.price, 2)}$ to fly from Mexico - MX to {record['city']}"
            msg2 = f" - {record['code']}, from {flight_search.outbound_date} to {flight_search.inbound_date}"
            msg = msg0 + msg1 + msg2
            print(msg)
            for email in emails:
                notification_manager.send_emails(email, msg)
                # notification_manager.send_message(msg)

        else:
            json_price = {"price": {"lowestPrice": round(price, 2)}}
            data_manager.update_information(record=int(record["id"]), json_data=json_price)
            record["price"] = price
            msg0 = "Subject: Flight Deal!\n\n"
            msg1 = f"Low Price Alert! Only {round(flight_search.price, 2)}$ to fly from Mexico - MX to {record['city']}"
            msg2 = f" - {record['code']}, from {flight_search.outbound_date} to {flight_search.inbound_date}"
            msg3 = f"\nFlight has 1 stop over, via {flight_search.via_city}."
            msg = msg0 + msg1 + msg2 + msg3
            print(msg)
            for email in emails:
                notification_manager.send_emails(email, msg)
            notification_manager.send_message(msg)
