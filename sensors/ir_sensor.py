import RPi.GPIO as GPIO
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import IR_SENSOR

GPIO.setmode(GPIO.BCM)
GPIO.setup(IR_SENSOR, GPIO.IN)

def detect_finger():
    return GPIO.input(IR_SENSOR) == 0

if __name__ == "__main__":
    try:
        while True:
            if detect_finger():
                print("Finger detected!")
            else:
                print("No finger detected.")
    except KeyboardInterrupt:
        GPIO.cleanup()
