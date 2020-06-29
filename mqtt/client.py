import paho.mqtt.client as mqtt
import time

CLIENT_ID = 'MEHAI_CLIENT_TEST'


def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)


def main():
    client = mqtt.Client(CLIENT_ID)
    client.on_message = on_message
    client.connect('test.mosquitto.org')
    client.loop_start()

    client.subscribe("mehai_topic_test")
    client.publish("mehai_topic_test", "this is my message")
    time.sleep(4)

    client.loop_stop()

    client.disconnect()

if __name__ == '__main__':
    main()