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

# Global Variables
weather_data = ""
news_headlines = []
current_news_index = 0

# Initialize Tkinter Window
root = tk.Tk()
root.title("Smart Mirror")
root.geometry("1280x1024")  # Adjust to screen size (Max 19 inches)
root.configure(bg="black")

# UI Labels
greeting_label = tk.Label(root, text="Hello!", font=("Helvetica", 24, "bold"), fg="white", bg="black")
greeting_label.pack(pady=10)

message_label = tk.Label(root, text="", font=("Helvetica", 18), fg="yellow", bg="black")
message_label.pack(pady=5)

weather_label = tk.Label(root, text="Loading weather...", font=("Helvetica", 20), fg="white", bg="black")
weather_label.pack(pady=10)

news_label = tk.Label(root, text="Loading news...", font=("Helvetica", 18), fg="cyan", bg="black", wraplength=600)
news_label.pack(pady=5)

calendar_label = tk.Label(root, text=get_calendar(), font=("Helvetica", 18), fg="white", bg="black", justify="left")
calendar_label.pack(pady=10)

temperature_label = tk.Label(root, text="Loading temperature...", font=("Helvetica", 20), fg="white", bg="black")
temperature_label.pack(pady=10)

heartbeat_label = tk.Label(root, text="Measuring heartbeat...", font=("Helvetica", 20), fg="white", bg="black")
heartbeat_label.pack(pady=10)

# Function to Update Greeting with Name & Emotion
def update_greeting():
    name, emotion, message = recognize_face()
    greeting_label.config(text=f"Hello, {name}!")
    message_label.config(text=message)
    root.after(10000, update_greeting)  # Run every 10 seconds

# Function to Update Weather
def update_weather():
    global weather_data
    weather_data = get_weather()
    weather_label.config(text=weather_data)
    root.after(600000, update_weather)  # Update every 10 minutes

# Function to Update News
def update_news():
    global current_news_index
    if news_headlines:
        news_label.config(text=news_headlines[current_news_index])
        current_news_index = (current_news_index + 1) % len(news_headlines)
    root.after(300000, update_news)  # Change news every 5 minutes

# Function to Fetch News Headlines
def fetch_news():
    global news_headlines
    news_headlines = get_news()
    update_news()

# Function to Update Temperature Data
def update_temperature():
    temp = read_temperature()
    temperature_label.config(text=f"Temperature: {temp}°C")
    root.after(5000, update_temperature)  # Update every 10 seconds

# Function to Update Heartbeat & SPO2 Data
def update_heartbeat():
    bpm, spo2 = get_heart_spo2()
    heartbeat_label.config(text=f"Heartbeat: {bpm} BPM | SpO2: {spo2}%")
    root.after(5000, update_heartbeat)  # Update every 10 seconds

# Function to Check Ultrasonic Sensor (Auto-Screen ON/OFF)
def check_ultrasonic_sensor():
    distance = get_distance()
    screen_on = distance < 50
    if screen_on:
        root.deiconify()  # Show Screen
    else:
        root.withdraw()  # Hide Screen
    root.after(2000, check_ultrasonic_sensor)  # Check every 2 sec

# Function to Check IR Sensor for Finger Detection & Start Countdown
def check_ir_sensor():
    finger_detected = detect_finger()
    if finger_detected:
        countdown_timer()
    root.after(1000, check_ir_sensor)  # Check every 1 sec

# Countdown Function for Finger Detection
def countdown_timer():
    for i in range(10, 0, -1):
        message_label.config(text=f"Please wait... {i} sec")
        root.update()
        time.sleep(1)
    message_label.config(text="Measurement complete!")

# Start All Updates
def start_updates():
    threading.Thread(target=fetch_news, daemon=True).start()
    update_greeting()
    update_weather()
    update_temperature()
    update_heartbeat()
    check_ultrasonic_sensor()
    check_ir_sensor()

# Run the App
start_updates()
root.mainloop()

