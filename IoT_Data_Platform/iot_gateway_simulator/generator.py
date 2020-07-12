import random

ROOM_LOW = 1
ROOM_HIGH = 6
TEMP_AVG = 20.0
HUM_AVG = 50
LIGHT_CHANGE_PROBABILITY = 0.1
CORRUPT_DATA_PROBABILITY = 0.05


class Generator:
    """
        The Generator can be used using the generate method which will
    return pseudo-random sensor data for the next room.

        The humidity and temperature will depend on the previous measurements
    generated for that room by changing with at most 1 / 2 points. The variance
    changes with the deviance of the value from the average value.
        The light represents the percentage of time since the last measurement
    in which the light was on. It also depends on the previous measurement for
    a specific room. The light has a 80% probability to remain unchanged for a
    room and a 10% to change to a random percentage from which it will change
    again to either 100% or 0%.
    """

    def __init__(self):
        self.cur_room = ROOM_LOW
        self.temperature = [20.0] * 6
        self.humidity = [50] * 6
        self.light = [100, 0, 0, 0, 100, 0]

    def __temperature(self, room):
        diff_from_avg = abs(self.temperature[room] - TEMP_AVG)
        variance = 1 - diff_from_avg / 10
        low_limit, high_limit = -1, 1
        if self.temperature[room] > TEMP_AVG:
            low_limit, high_limit = -1, variance
        else:
            low_limit, high_limit = -variance, 1
        self.temperature[room] += random.uniform(low_limit, high_limit)
        self.temperature[room] = round(self.temperature[room], 1)
        return self.temperature[room]

    def __humidity(self, room):
        diff_from_avg = abs(self.humidity[room] - HUM_AVG)
        variance = 2 - diff_from_avg / 10
        low_limit, high_limit = -2, 2
        if self.humidity[room] > HUM_AVG:
            low_limit, high_limit = -2, variance
        else:
            low_limit, high_limit = -variance, 2
        self.humidity[room] += random.uniform(low_limit, high_limit)
        self.humidity[room] = int(round(self.humidity[room], 0))
        return self.humidity[room]

    def __light(self, room):
        cur_light = self.light[room]
        if cur_light == 0 or cur_light == 100:
            if random.random() <= LIGHT_CHANGE_PROBABILITY:
                self.light[room] = round(random.uniform(0, 100), 0)
        else:
            self.light[room] = random.choice((0, 100))
        return self.light[room]

    def generate(self) -> tuple:
        room = self.cur_room - 1
        self.cur_room = self.cur_room % 6 + 1
        if random.random() <= CORRUPT_DATA_PROBABILITY:
            return room + 1, None, 100, 0
        return (room + 1,
                self.__temperature(room),
                self.__humidity(room),
                self.__light(room))
