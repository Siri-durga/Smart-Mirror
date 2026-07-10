import tkinter as tk
from time import strftime
from api.weather import get_weather
from api.news import get_news
from sensors.temperature import read_temperature
from sensors.max30100_sensor import read_max30100
from face_recognition.recognition import recognize_face

def update_ui(root, labels):
    labels['time'].config(text=strftime('%H:%M:%S %p'))
    labels['date'].config(text=strftime('%A, %B %d, %Y'))
    labels['weather'].config(text=get_weather())
    labels['news'].config(text=get_news())

    labels['temperature'].config(text=f"Temperature: {read_temperature()}")
    heartbeat, spo2 = read_max30100()
    labels['heartbeat'].config(text=f"Heartbeat: {heartbeat}")
    labels['spo2'].config(text=f"SPO2: {spo2}")

    user, emotion = recognize_face()
    labels['greeting'].config(text=f"Hello, {user}!")
    emotion_messages = {
        "happy": "Have a joyful day! 😊",
        "neutral": "Stay positive and keep smiling! 😎",
        "sad": "Hope you feel better soon! 💙"
    }
    labels['message'].config(text=emotion_messages.get(emotion, "Welcome!"))

    root.after(5000, update_ui, root, labels)
