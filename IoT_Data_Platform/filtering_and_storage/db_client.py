import psycopg2
import json
import time

query_enable_timescaledb_extension = """
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
"""

query_create_rooms_table = """
CREATE TABLE IF NOT EXISTS room (
                                    id INTEGER PRIMARY KEY,
                                    name VARCHAR(50)
                                );
"""

query_create_sensors_table = """
CREATE TABLE IF NOT EXISTS sensor_data (
                                       time TIMESTAMPTZ NOT NULL,
                                       room_id INTEGER,
                                       temperature FLOAT,
                                       humidity INTEGER,
                                       light INTEGER,
                                       FOREIGN KEY (room_id) REFERENCES room (id)
                                   );
"""

query_create_sensors_hypertable = """
SELECT create_hypertable('sensor_data', 'time', if_not_exists => true);
"""

query_insert_rooms = """
INSERT INTO room (id, name) VALUES (%s, %s) ON CONFLICT (id) DO NOTHING;
"""

query_insert_sensor_data = """
INSERT INTO sensor_data (time, room_id, temperature, humidity, light) VALUES (NOW(), %s, %s, %s, %s);
"""


class DBConnector:
    """
        This connects to a TimescaleDB at given host, creates the necessary objects if they don't exist and can
    be externally used through the insert function.
    """
    def __init__(self, host, user, passw, db_name):
        self.CONNECTION = "postgres://{}:{}@{}/{}"
        self.host = host
        self.user = user
        self.passw = passw
        self.db_name = db_name
        self.conn = self.__connect()
        # wait until db is ready and connection is accepted
        while self.conn is None:
            print('Connection could not be established...')
            time.sleep(5)
            self.conn = self.__connect()
        print('Connection to the database succeded!')
        self.__create_tables()
        self.__init_tables()

    def __create_tables(self):
        cur = self.conn.cursor()
        cur.execute(query_enable_timescaledb_extension)
        cur.execute(query_create_rooms_table)
        cur.execute(query_create_sensors_table)
        cur.execute(query_create_sensors_hypertable)
        self.conn.commit()
        cur.close()

    def __init_tables(self):
        cur = self.conn.cursor()
        rooms = [(1, 'hallway'),
                 (2, 'kitchen'),
                 (3, 'bathroom'),
                 (4, 'main bedroom'),
                 (5, 'second bedroom'),
                 (6, 'guestroom')]
        for room in rooms:
            try:
                cur.execute(query_insert_rooms, room)
            except (Exception, psycopg2.Error) as error:
                print(error.pgerror)
        self.conn.commit()
        cur.close()

    def __connect(self):
        try:
            conn_str = self.CONNECTION.format(self.user, self.passw, self.host, self.db_name)
            return psycopg2.connect(conn_str)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)

    def insert(self, json_obj):
        #print(json.dumps(json_obj, indent=4))
        cur = self.conn.cursor()
        data = [json_obj['room'],
                json_obj['values']['temperature'],
                json_obj['values']['humidity'],
                json_obj['values']['light']]
        try:
            cur.execute(query_insert_sensor_data, data)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
        self.conn.commit()
        cur.close()
