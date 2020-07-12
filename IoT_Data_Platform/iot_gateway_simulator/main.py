from generator import Generator
from publisher import Publisher
import json


def main(generator: Generator, publisher: Publisher) -> int:
    print("IoT Gateway (Simulator)")
    print("=======================")
    while True:
        r, t, h, l = generator.generate()
        json_obj = {'room': r,
                    'values': {
                        'temperature': t,
                        'humidity': h,
                        'light': l
                    }}
        json_str = json.dumps(json_obj, indent=4)
        publisher.send(json_str)
        cmd = input("What do you want to do next?\nq - quit\nanything else - continue.")
        if cmd == 'q':
            break
    return 0


if __name__ == '__main__':
    gen = Generator()
    pub = Publisher()
    main(gen, pub)
    pub.end_connection()
