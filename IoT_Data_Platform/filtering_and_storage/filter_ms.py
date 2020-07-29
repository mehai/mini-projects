import json

ROOM_LOW = 1
ROOM_HIGH = 6
TEMP_LOW = 0
TEMP_HIGH = 40
HUM_LOW = 0
HUM_HIGH = 100
LIGHT_LOW = 0
LIGHT_HIGH = 100


class Filter:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def filter(self, message: str):
        try:
            jsonObj = json.loads(message)
            print(jsonObj)
            if isinstance(jsonObj, dict):
                if jsonObj['room'] is None or jsonObj['room'] < ROOM_LOW or jsonObj['room'] > ROOM_HIGH:
                    raise ValueError
                if not isinstance(jsonObj['values'], dict):
                    raise json.JSONDecodeError
                values = jsonObj['values']
                if values['temperature'] is None or \
                   values['temperature'] < TEMP_LOW or values['temperature'] > TEMP_HIGH:
                    raise ValueError
                if values['humidity'] is None or \
                   values['humidity'] < HUM_LOW or values['humidity'] > HUM_HIGH:
                    raise ValueError
                if values['light'] is None or \
                   values['light'] < LIGHT_LOW or values['light'] > LIGHT_HIGH:
                    raise ValueError
                print('calling db_connector for insert')
                self.db_connector.insert(jsonObj)
            else:
                raise json.JSONDecodeError
        except json.JSONDecodeError:
            print(f"Not what was expected: {message}")
        except ValueError:
            print(f"Integrity errors for: {message}")

