from subscriber import Subscriber
from filter_ms import Filter
from db_client import DBConnector
import time


def main(subscriber):
    while True:
        time.sleep(5)
        cmd = input("Would you like to quit? y/n")
        if cmd == 'y':
            subscriber.end_connection()


if __name__ == '__main__':
    sub = Subscriber(Filter(DBConnector()))
    main(sub)
