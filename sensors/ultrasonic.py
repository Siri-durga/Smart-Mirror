import time
import RPi.GPIO as GPIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import TRIG, ECHO

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    distance = (stop_time - start_time) * 17150
    return round(distance, 2)

if __name__ == "__main__":
    try:
        while True:
            print(f"Distance: {get_distance()} cm")
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
