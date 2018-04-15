from datetime import datetime
import random


def get_data():
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cpu_temp = 30+random.randint(-10, 15)
    outside_temp = 10+random.randint(-20, 25)
    pressure = 980+random.randint(0, 20)
    humidity = 30+random.randint(0, 70)
    flow = 8+random.random()
    level = 85-random.randint(0, 5)

    ret = {
        'time': time,
        'cpu_temperature': cpu_temp,
        'outside_temperature': outside_temp,
        'pressure': pressure,
        'humidity': humidity,
        'flow': flow,
        'level': level
    }
    return ret

