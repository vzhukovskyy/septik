from gpiozero import CPUTemperature
from bme280.bme280 import readBME280All
import RPi.GPIO as GPIO
import os, time, signal, datetime

TIMER_DELAY = 1
FLOW_SENSOR_GPIO_TRIGGER = 18
FLOW_SENSOR_GPIO_ECHO = 27
LEVEL_SENSOR_GPIO_TRIGGER = 5
LEVEL_SENSOR_GPIO_ECHO = 6

# Speed of sound in cm/s at temperature
temperature = 10
speedSound = 33100 + (0.6*temperature)

def init():
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

def measure_distance(gpio_trigger, gpio_echo):
    # Send 10us pulse to trigger
    GPIO.output(gpio_trigger, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(gpio_trigger, False)
    start = time.time()
    pulse_start = start

    while GPIO.input(gpio_echo)==0:
      pulse_start = time.time()
      # avoid hangup
      if pulse_start - start > 0.1:
          return 0

    pulse_stop = time.time()
    while GPIO.input(gpio_echo)==1:
      pulse_stop = time.time()
      # avoid hangup
      if pulse_stop - pulse_start > 0.1:
          return 0

    elapsed = pulse_stop - pulse_start
    distance = elapsed * speedSound
    distance = distance / 2
    
    return distance

def get_sensor_data():
    time = datetime.datetime.now()
    cputemp = CPUTemperature().temperature
    temperature,pressure,humidity = readBME280All()
    distance_flow_sensor = measure_distance(gpio_trigger=FLOW_SENSOR_GPIO_TRIGGER, gpio_echo=FLOW_SENSOR_GPIO_ECHO)
    distance_level_sensor = measure_distance(gpio_trigger=LEVEL_SENSOR_GPIO_TRIGGER, gpio_echo=LEVEL_SENSOR_GPIO_ECHO)
    return time,cputemp,temperature,pressure,humidity,distance_flow_sensor,distance_level_sensor

#
init()
