import sys
import random
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import TEMP_SENSOR_PATH

def read_temperature():
    try:
        with open(TEMP_SENSOR_PATH, 'r') as file:
            lines = file.readlines()
            temp_str = lines[1].split("t=")[-1]
            return round(int(temp_str) / 1000.0, 1)
    except:
        return random.randint(32, 38)

if __name__ == "__main__":
    print(f"Temperature: {read_temperature()}C")
