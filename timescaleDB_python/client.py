import psycopg2
from pgcopy import CopyManager

# CONNECTION = "postgres://username:password@host:port/dbname?sslmode=require"
CONNECTION = "postgres://{}:{}@localhost:5432/{}?sslmode=require"

query_create_sensors_table = """CREATE TABLE IF NOT EXISTS sensors (
                                    id SERIAL PRIMARY KEY,
                                    type VARCHAR(50),
                                    location VARCHAR(50)
                                );"""

query_create_sensordata_table = """CREATE TABLE IF NOT EXISTS sensor_data (
                                       time TIMESTAMPTZ NOT NULL,
                                       sensor_id INTEGER,
                                       temperature DOUBLE PRECISION,
                                       cpu DOUBLE PRECISION,
                                       FOREIGN KEY (sensor_id) REFERENCES sensors (id)
                                   );"""

query_create_sensordata_hypertable = """SELECT create_hypertable('sensor_data', 'time', if_not_exists => true);"""


def create_table(connection):
    cur = connection.cursor()
    cur.execute(query_create_sensors_table)
    connection.commit()
    cur.close()


def create_hypertable(connection):
    cur = connection.cursor()
    cur.execute(query_create_sensordata_table)
    cur.execute(query_create_sensordata_hypertable)
    connection.commit()
    cur.close()


def check_sensors(connection):
    """ Returns true if there are more than 0 rows in the sensors table."""
    cur = connection.cursor()
    cur.execute("SELECT COUNT(*) FROM sensors;")
    result = cur.fetchall()[0][0]
    cur.close()
    return result > 0


def insert_sensors(connection):
    """ Inserts 4 sensors if there are currently none in the sensors table."""
    if check_sensors(connection):
        return
    sensors = [('a', 'floor'), ('a', 'ceiling'), ('b', 'floor'), ('b', 'ceiling')]
    insert_sensors_query = "INSERT INTO sensors (type, location) VALUES (%s, %s);"
    cur = connection.cursor()
    for sensor in sensors:
        try:
            data = (sensor[0], sensor[1])
            cur.execute(insert_sensors_query, data)
        except (Exception, psycopg2.Error) as error:
            print(error.pgerror)
    connection.commit()
    cur = connection.cursor()
    cur.close()


def insert_random_data(connection):
    cur = connection.cursor()
    for sensor_id in range(1, 4, 1):
        data = (sensor_id,)
        # create random data
        simulate_query = """SELECT  generate_series(now() - interval '24 hour', now(), interval '5 minute') AS time,
           %s as sensor_id,
           random()*100 AS temperature,
           random() AS cpu
           """
        cur.execute(simulate_query, data)
        values = cur.fetchall()
        # define columns names of the table you're inserting into
        cols = ('time', 'sensor_id', 'temperature', 'cpu')
        # create copy manager with the target table and insert!
        mgr = CopyManager(connection, 'sensor_data', cols)
        mgr.copy(values)
    # commit after all sensor data is inserted
    connection.commit()


def query_generated_data(connection):
    cur = connection.cursor()
    query = "SELECT * FROM sensor_data;"
    cur.execute(query)
    for i in cur.fetchall():
        print(i)
    cur.close()


def main(user, password, db_name):
    conn_str = CONNECTION.format(user, password, db_name)
    # connect to db
    with psycopg2.connect(conn_str) as conn:
        create_table(conn)
        insert_sensors(conn)
        create_hypertable(conn)
        insert_random_data(conn)
        query_generated_data(conn)


if __name__ == '__main__':
    print("Please provide credentials for DB connection.")
    user = input("Username: ")
    password = input("Password: ")
    db_name = input("Database name: ")
    main(user, password, db_name)
