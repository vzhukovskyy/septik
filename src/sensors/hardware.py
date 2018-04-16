import time, datetime
from gpiozero import CPUTemperature
from bme280.bme280 import readBME280All
from distance import distance
import RPi.GPIO as GPIO


FLOW_SENSOR_GPIO_TRIGGER = 18
FLOW_SENSOR_GPIO_ECHO = 27
LEVEL_SENSOR_GPIO_TRIGGER = 5
LEVEL_SENSOR_GPIO_ECHO = 6


def _init():
    # Use BCM GPIO references instead of physical pin numbers
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FLOW_SENSOR_GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(FLOW_SENSOR_GPIO_ECHO, GPIO.IN)
    GPIO.setup(LEVEL_SENSOR_GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(LEVEL_SENSOR_GPIO_ECHO, GPIO.IN)

    GPIO.output(FLOW_SENSOR_GPIO_TRIGGER, False)
    GPIO.output(LEVEL_SENSOR_GPIO_TRIGGER, False)

    # Allow module to settle
    time.sleep(0.5)


def get_data():
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    cpu_temp = CPUTemperature().temperature
    outside_temp, pressure, humidity = readBME280All()
    flow = distance.measure_distance(gpio_trigger=FLOW_SENSOR_GPIO_TRIGGER, gpio_echo=FLOW_SENSOR_GPIO_ECHO)
    level = distance.measure_distance(gpio_trigger=LEVEL_SENSOR_GPIO_TRIGGER, gpio_echo=LEVEL_SENSOR_GPIO_ECHO)

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


_init()
