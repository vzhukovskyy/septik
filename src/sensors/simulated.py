import random
from src.utils.timeutil import timeutil


def get_data():
    time = timeutil.sensors_now()
    cpu_temp = 30+random.random()*2
    outside_temp = 10+random.random()*2
    pressure = 980+random.random()*5
    humidity = 30+random.random()*5
    flow = 8+random.random()
    level = 85-random.random()*5

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

