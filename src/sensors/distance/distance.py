import time
import RPi.GPIO as GPIO

# Speed of sound in cm/s at temperature
temperature = 10
speedSound = 33100 + (0.6*temperature)

def measure_distance(gpio_trigger, gpio_echo):
    # Send 10us pulse to trigger
    GPIO.output(gpio_trigger, True)
    # Wait 10us
    time.sleep(0.00001)
    GPIO.output(gpio_trigger, False)
    start = time.time()
    pulse_start = start

    while GPIO.input(gpio_echo) == 0:
        pulse_start = time.time()
        # avoid hangup
        if pulse_start - start > 0.1:
            return 0

    pulse_stop = time.time()
    while GPIO.input(gpio_echo) == 1:
        pulse_stop = time.time()
        # avoid hangup
        if pulse_stop - pulse_start > 0.1:
            return 0

    elapsed = pulse_stop - pulse_start
    distance = elapsed * speedSound
    distance = distance / 2

    return distance