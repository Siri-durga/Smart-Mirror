import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from max30100 import MAX30100  

max30100 = MAX30100()
max30100.enable_spo2()

def get_heart_spo2():
    max30100.read_sensor()
    return round(max30100.ir / 100, 1), round(max30100.red / 100, 1)

if __name__ == "__main__":
    try:
        while True:
            heartbeat, spo2 = get_heart_spo2()
            print(f"Heartbeat: {heartbeat} BPM, SPO2: {spo2} %")
    except KeyboardInterrupt:
        pass
