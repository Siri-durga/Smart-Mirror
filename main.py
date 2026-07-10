import tkinter as tk
import time
import threading
from datetime import datetime
from face_recognition.recognition import recognize_face
from api.weather import get_weather
from api.news import get_news
from ui.calendar import get_calendar
from sensors.ultrasonic import get_distance
from sensors.ir_sensor import detect_finger
from sensors.temperature import read_temperature
from sensors.max30100_sensor import get_heart_spo2
from PIL import Image, ImageTk

# Global Variables
weather_data = ""
news_headlines = []
current_news_index = 0
heartbeat_value = "--"
spo2_value = "--"
temperature_value = "--"

# Initialize Tkinter Window
root = tk.Tk()
root.title("Smart Mirror")
root.geometry("1280x1024")  # Adjust to screen size
root.configure(bg="black")

# UI Layout
header_frame = tk.Frame(root, bg="black")
header_frame.pack(fill=tk.X, pady=10)

datetime_label = tk.Label(header_frame, text="", font=("Helvetica", 20), fg="white", bg="black")
datetime_label.pack(side=tk.LEFT, padx=20)

weather_label = tk.Label(header_frame, text="Loading weather...", font=("Helvetica", 20), fg="white", bg="black")
weather_label.pack(side=tk.RIGHT, padx=20)

content_frame = tk.Frame(root, bg="black")
content_frame.pack(expand=True, fill=tk.BOTH)

greeting_label = tk.Label(content_frame, text="Hello!", font=("Helvetica", 24, "bold"), fg="white", bg="black")
greeting_label.pack(pady=10)

calendar_label = tk.Label(content_frame, text=get_calendar(), font=("Helvetica", 18), fg="white", bg="black")
calendar_label.pack(pady=10)

news_label = tk.Label(content_frame, text="Loading news...", font=("Helvetica", 18), fg="cyan", bg="black", wraplength=600)
news_label.pack(pady=5)

# Sensor Data Cards
sensor_frame = tk.Frame(root, bg="black")
sensor_frame.pack(side=tk.BOTTOM, pady=10)

#temp_icon = ImageTk.PhotoImage(Image.open("icons/temp.png").resize((30, 30)))
temp_label = tk.Label(sensor_frame, text=f"🌡 Temp: {temperature_value}°C", font=("Helvetica", 18), fg="white", bg="black")
temp_label.pack(side=tk.LEFT, padx=10)

#heart_icon = ImageTk.PhotoImage(Image.open("icons/heart.png").resize((30, 30)))
heartbeat_label = tk.Label(sensor_frame, text=f"❤️ Heart: {heartbeat_value} BPM", font=("Helvetica", 18), fg="white", bg="black")
heartbeat_label.pack(side=tk.LEFT, padx=10)

#spo2_icon = ImageTk.PhotoImage(Image.open("icons/spo2.png").resize((30, 30)))
spo2_label = tk.Label(sensor_frame, text=f"🩸 SpO2: {spo2_value}%", font=("Helvetica", 18), fg="white", bg="black")
spo2_label.pack(side=tk.LEFT, padx=10)

# Function to Update Date & Time
def update_datetime():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datetime_label.config(text=now)
    root.after(1000, update_datetime)

# Function to Update Greeting
def update_greeting():
    name, _, message = recognize_face()
    greeting_label.config(text=f"Hello, {name}! {message}")
    root.after(10000, update_greeting)

# Function to Update Weather
def update_weather():
    global weather_data
    weather_data = get_weather()
    weather_label.config(text=weather_data)
    root.after(600000, update_weather)

# Function to Update News
def update_news():
    global current_news_index
    if news_headlines:
        news_text = "\n".join(news_headlines[:3])  # Show 3 headlines
        news_label.config(text=news_text)
        current_news_index = (current_news_index + 1) % len(news_headlines)
    root.after(300000, update_news)

# Function to Fetch News
def fetch_news():
    global news_headlines
    news_headlines = get_news()
    update_news()

# Function to Update Sensor Data
def update_sensors():
    global temperature_value, heartbeat_value, spo2_value
    temp = read_temperature()
    temperature_value = temp
    temp_label.config(text=f"🌡 Temp: {temp}°C")
    
    bpm, spo2 = get_heart_spo2()
    heartbeat_value = bpm if bpm else "--"
    spo2_value = spo2 if spo2 else "--"
    heartbeat_label.config(text=f"❤️ Heart: {heartbeat_value} BPM")
    spo2_label.config(text=f"🩸 SpO2: {spo2_value}%")
    
    root.after(5000, update_sensors)

# Function to Check Ultrasonic Sensor
def check_ultrasonic_sensor():
    distance = get_distance()
    if distance > 50:
        root.withdraw()  # Hide screen
    else:
        root.deiconify()  # Show screen
    root.after(2000, check_ultrasonic_sensor)

# Function to Check IR Sensor
def check_ir_sensor():
    finger_detected = detect_finger()
    if finger_detected:
        start_countdown()
    root.after(1000, check_ir_sensor)

# Countdown Function
def start_countdown():
    global heartbeat_value, spo2_value
    heartbeat_label.config(text="❤️ Heart: -- BPM")
    spo2_label.config(text="🩸 SpO2: --%")
    for i in range(10, 0, -1):
        news_label.config(text=f"Please wait... {i} sec")
        root.update()
        time.sleep(1)
    news_label.config(text="Measurement complete!")
    update_sensors()

# Start Updates
def start_updates():
    threading.Thread(target=fetch_news, daemon=True).start()
    update_datetime()
    update_greeting()
    update_weather()
    update_sensors()
    check_ultrasonic_sensor()
    check_ir_sensor()

# Run the App
start_updates()
root.mainloop()
