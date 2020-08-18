import paho.mqtt.client as mqtt
from filter_ms import Filter
import os


class Subscriber:
    CLIENT_ID = 'Filtering_Microservice'
    BROKER_IP = os.getenv('BROKER_IP')

    def __init__(self, filter_service: Filter):
        self.filter_service = filter_service
        self.client = mqtt.Client(Subscriber.CLIENT_ID)
        self.client.on_message = self.on_message
        self.client.connect(Subscriber.BROKER_IP)
        self.client.subscribe("home")
        self.client.loop_forever(retry_first_connection=True)

    def on_message(self, client, userdata, message):
        self.filter_service.filter(str(message.payload.decode("utf-8")))

    def end_connection(self):
        self.client.disconnect()
