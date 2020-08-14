from subscriber import Subscriber
from filter_ms import Filter
from db_client import DBConnector
from get_docker_secret import get_docker_secret
import time
import os


if __name__ == '__main__':
    tsdb_host = os.getenv('TSDB_HOST')
    tsdb_user = get_docker_secret(os.getenv('TSDB_USER'), default='test')
    tsdb_password = get_docker_secret(os.getenv('TSDB_PASSWORD'), default='test')
    tsdb_db = os.getenv('TSDB_DB')
    sub = Subscriber(Filter(DBConnector(tsdb_host, tsdb_user, tsdb_password, tsdb_db)))
