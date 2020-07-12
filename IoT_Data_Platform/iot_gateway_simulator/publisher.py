import paho.mqtt.client as mqtt


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


class Publisher:
    CLIENT_ID = 'IoT_Gateway'
    BROKER_IP = '127.0.0.1'

    def __init__(self):
        self.client = mqtt.Client(Publisher.CLIENT_ID)
        self.client.on_message = on_message
        self.client.connect(Publisher.BROKER_IP)
        self.client.subscribe("home")

    def send(self, data):
        print(data)
        self.client.loop_start()
        self.client.publish("home", data)
        self.client.loop_stop()

    def end_connection(self):
        self.client.disconnect()
