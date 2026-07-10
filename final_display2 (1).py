import tkinter as tk
from sensors.ultrasonic import get_distance  # Ultrasonic sensor function
import time
import calendar
from datetime import datetime
import math
from api.weather import get_weather
from api.news import get_news
from sensors.temperature import read_temperature
from sensors.max30100_sensor import get_heart_spo2
from sensors.ir_sensor import detect_finger

# Initialize global variables
finger_detected = False
countdown = 10

# def update_greeting():
#     name, emotion, message = recognize_face()
#     greeting_label.config(text=f"Hello, {name}!")
#     message_label.config(text=message)
#     root.after(10000, update_greeting)  # Run every 10 seconds


def update_display():
    """Check the distance and update the screen."""
    distance = get_distance()
    if distance < 50:
        show_clock_and_calendar()
    else:
        hide_clock_and_calendar()

    root.after(1000, update_display)  # Run again after 1 second

def show_clock_and_calendar():
    """Show the clock and calendar when a person is detected."""
    draw_clock()  # Update clock hands
    time_label.config(text=time.strftime("%H:%M:%S"))  # Update digital time

    # Show elements
    clock_canvas.place(x=screen_width - 220, y=20)
    time_label.place(x=screen_width - 180, y=210)
    weather_label.place(x=20, y=20)  # Show weather above the month title
    month_title.place(x=80, y=80)
    cal_frame.place(x=20, y=130)
    news_label.place(x=screen_width // 2, y=800, anchor="center")
    canvas.place(x=screen_width - 180, y=600, anchor="center")
    greeting_label.place(x=screen_width // 2, y=50, anchor="center") 
    message_label.place(x=screen_width // 2, y=80, anchor="center")
    


def hide_clock_and_calendar():
    """Hide all elements when no person is detected."""
    greeting_label.place_forget()
    message_label.place_forget()
    clock_canvas.place_forget()
    time_label.place_forget()
    month_title.place_forget()
    cal_frame.place_forget()
    weather_label.place_forget()
    news_label.place_forget()
    canvas.place_forget()
    

def draw_clock():
    """Draw an analog clock with hour, minute, and second hands."""
    clock_canvas.delete("all")  # Clear previous drawings

    # Draw clock face
    clock_canvas.create_oval(10, 10, 180, 180, outline="white", width=3)

    # Get current time
    now = datetime.now()
    hr, min, sec = now.hour % 12, now.minute, now.second
    
    # Convert to angles
    sec_angle = (sec / 60) * 360
    min_angle = (min / 60) * 360
    hr_angle = ((hr + min / 60) / 12) * 360

    # Draw clock hands
    draw_hand(hr_angle, 50, "white", 6)   # Hour hand
    draw_hand(min_angle, 65, "yellow", 4)  # Minute hand
    draw_hand(sec_angle, 75, "red", 2)    # Second hand

    # Redraw every second
    root.after(1000, draw_clock)
    
def draw_hand(angle, length, color, width):
    """Helper function to draw a clock hand based on angle."""
    x_center, y_center = 95, 95  # Clock center
    angle_rad = math.radians(angle - 90)
    x_end = x_center + length * math.cos(angle_rad)
    y_end = y_center + length * math.sin(angle_rad)
    clock_canvas.create_line(x_center, y_center, x_end, y_end, fill=color, width=width)
    
def update_sensors():
    """Fetch and update sensor readings for temperature, heart rate, and SpO2 after 10 seconds if a finger is detected."""
    global countdown, finger_detected
    
    # Check for finger detection
    if detect_finger():
        finger_detected = True
        clock_canvas.place(x=screen_width - 220, y=20)
        time_label.place(x=screen_width - 180, y=210)
        weather_label.place(x=20, y=20)  # Show weather above the month title
        month_title.place(x=80, y=80)
        cal_frame.place(x=20, y=130)
        news_label.place(x=screen_width // 2, y=800, anchor="center")
        sensor_frame.place(x=screen_width // 2, y=600., anchor="center")  # Center placement
        canvas.place(x=screen_width - 180, y=600, anchor="center")
        greeting_label.place(x=screen_width // 2, y=50, anchor="center") 
        message_label.place(x=screen_width // 2, y=80, anchor="center")
        countdown_label.place(relx=0.5, rely=0.5, anchor="center")  # Center position
        countdown_label.config(text="10s")  # Start Timer Display
        countdown_timer()
    else:
        finger_detected = False
        sensor_frame.place_forget()
        countdown_label.place_forget()
        reset_display()  # Keep values as "--" if no finger is detected

    # Refresh every 5 seconds to check for a finger again
    root.after(5000, update_sensors)

def countdown_timer():
    """Handles the countdown before displaying sensor values."""
    global countdown

    if countdown > 0:
        countdown_label.config(text=f"{countdown}s")
        countdown -= 1
        root.after(1000, countdown_timer)  # Update timer every second
    else:
        display_sensor_values()  # Show sensor values after countdown
        
def display_sensor_values():
    """Fetch and display sensor readings after countdown ends."""
    try:
        temperature = read_temperature()
        heart_rate, spo2 = get_heart_spo2()

        # Update labels with real values
        temp_value_label.config(text=f"{temperature:.1f}C")
        heart_value_label.config(text=f"{heart_rate} BPM")
        spo2_value_label.config(text=f"{spo2}%")
    except Exception:
        temp_value_label.config(text="N/A")
        heart_value_label.config(text="N/A")
        spo2_value_label.config(text="N/A")

    countdown_label.config(text="")  # Hide countdown


def reset_display():
    """Reset sensor values to '--' if no finger is detected."""
    global countdown
    countdown = 10  # Reset countdown
    countdown_label.config(text="")  # Hide countdown
    temp_value_label.config(text="--")
    heart_value_label.config(text="--")
    spo2_value_label.config(text="--")
def update_weather():
    """Fetch and display the weather information with an icon."""
    weather_info = get_weather()
    if weather_info:
        condition, temperature = weather_info
        icon = get_weather_icon(condition)
        weather_label.config(text=f"{icon} {temperature:.1f}C | {condition.capitalize()}")
    else:
        weather_label.config(text="Weather data unavailable")  # Show an error message

    root.after(1800000, update_weather)  # Refresh every 30 min

def update_news():
    news = get_news()
    print("Fetched news:", news)  # Debugging
    if news:
        cycle_news(news, 0)
    else:
        news_label.config(text="No news available")
        
def fetch_news_async():
    threading.Thread(target=update_news, daemon=True).start()

    root.after(5000, fetch_news_async)  # Fetch news after 5 seconds

    
def cycle_news(news_list, index):
    print(f"Displaying news: {news_list[index]}")  # Debugging
    news_label.config(text=news_list[index], font=("Arial", 18), fg="white", bg="black")
    next_index = (index + 1) % len(news_list)
    root.after(5000, lambda: cycle_news(news_list, next_index))  # Change every 5 seconds


def get_weather_icon(condition):
    """Return an appropriate weather emoji based on condition."""
    condition = condition.lower()
    if "clear" in condition:
        return "\U00002600"  # ??
    elif "rain" in condition:
        return "\U0001F327"  # ??
    elif "cloud" in condition:
        return "\U00002601"  # ??
    elif "thunderstorm" in condition:
        return "\U000026C8"  # ?
    elif "snow" in condition:
        return "\U00002744"  # ??
    elif "mist" in condition or "fog" in condition:
        return "\U0001F32B"  # ??
    else:
        return "\U0001F324"  # ?? Default unknown

def create_calendar():
    """Create a static calendar."""
    today = datetime.today()
    year, month, day = today.year, today.month, today.day

    # Set the month title
    month_title.config(text=f"{calendar.month_name[month]} {year}")

    # Clear previous calendar grid
    for widget in cal_frame.winfo_children():
        widget.destroy()

    # Add day labels
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for col, day_name in enumerate(days):
        tk.Label(cal_frame, text=day_name, font=("Arial", 14, "bold"), 
                 bg="black", fg="white", padx=5, pady=5).grid(row=0, column=col, sticky="nsew")

    # Get the calendar matrix
    month_calendar = calendar.monthcalendar(year, month)

    # Add dates
    for row, week in enumerate(month_calendar, start=1):
        for col, date in enumerate(week):
            if date == 0:
                tk.Label(cal_frame, text=" ", bg="black", padx=10, pady=5).grid(row=row, column=col)
            else:
                is_today = (date == day)
                tk.Label(cal_frame, text=str(date), font=("Arial", 14, "bold" if is_today else "normal"),
                         bg="black", fg="gold" if is_today else "white",
                         padx=10, pady=5).grid(row=row, column=col, sticky="nsew")

# Initialize Tkinter
root = tk.Tk()
screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()

# Common Style
FONT_LARGE = ("Arial", 30, "bold")
FONT_MEDIUM = ("Arial", 22)
BG_COLOR = "black"
FG_COLOR = "white"

# Unicode Icons
TEMP_ICON = "\U0001F321"  # ?? Thermometer
HEART_ICON = "\u2764"  # ?? Heart
LUNGS_ICON = "\U0001FAC1"  # ?? Lungs

# Fullscreen setup
root.geometry(f"{screen_width}x{screen_height}")
root.config(bg="black")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))  # Exit fullscreen on Esc

# Clock Canvas
clock_canvas = tk.Canvas(root, width=200, height=200, bg="black", highlightthickness=0)

# Digital Time Label
time_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="black", fg="white")

# Month Label
month_title = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="black", fg="white")

# Weather Label (Positioned above month title)
weather_label = tk.Label(root, text="", font=("Arial", 20, "bold"), bg="black", fg="white")

#Greeting label
greeting_label = tk.Label(root, text="Good Afternoon Rohith", font=("Arial", 20, "bold"), bg="black", fg="white")

#message label
message_label = tk.Label(root, text="You are looking great today.", font=("Arial", 18), bg="black", fg="white")

# Calendar Frame
cal_frame = tk.Frame(root, bg="black")

# News Label
news_label = tk.Label(root, text="", font=("Arial", 18), bg="black", fg="white")

# Create the calendar
create_calendar()

# Frame for Sensor Data
sensor_frame = tk.Frame(root, bg=BG_COLOR)

# Temperature Card
temp_card = tk.Frame(sensor_frame, bg="#222222", padx=20, pady=20, bd=5, relief="ridge")
temp_card.grid(row=0, column=0, padx=15)
temp_label = tk.Label(temp_card, text="Temperature", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
temp_label.pack()
temp_icon_label = tk.Label(temp_card, text=TEMP_ICON, font=FONT_LARGE, fg="red", bg="#222222")
temp_icon_label.pack()
temp_value_label = tk.Label(temp_card, text="--C", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
temp_value_label.pack()

# Heart Rate Card
heart_card = tk.Frame(sensor_frame, bg="#222222", padx=20, pady=20, bd=5, relief="ridge")
heart_card.grid(row=0, column=1, padx=15)
heart_label = tk.Label(heart_card, text="Heart Rate", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
heart_label.pack()
heart_icon_label = tk.Label(heart_card, text=HEART_ICON, font=FONT_LARGE, fg="red", bg="#222222")
heart_icon_label.pack()
heart_value_label = tk.Label(heart_card, text="-- BPM", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
heart_value_label.pack()

# SpO2 Card
spo2_card = tk.Frame(sensor_frame, bg="#222222", padx=20, pady=20, bd=5, relief="ridge")
spo2_card.grid(row=0, column=2, padx=15)
spo2_label = tk.Label(spo2_card, text="SpO2 Level", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
spo2_label.pack()
spo2_icon_label = tk.Label(spo2_card, text=LUNGS_ICON, font=FONT_LARGE, fg="cyan", bg="#222222")
spo2_icon_label.pack()
spo2_value_label = tk.Label(spo2_card, text="--%", font=FONT_MEDIUM, fg=FG_COLOR, bg="#222222")
spo2_value_label.pack()

# Countdown Timer Label (Appears only when finger is detected)
countdown_label = tk.Label(root, text="", font=("Arial", 28, "bold"), fg="yellow", bg="black")

# Create canvas
canvas = tk.Canvas(root, width=200, height=100, bg="black", highlightthickness=0)

# Add text above the arrow
canvas.create_text(100, 20, text="Place finger here", font=("Arial", 16, "bold"), fill="white")

# Draw an arrow
canvas.create_line(30, 60, 170, 60, arrow=tk.LAST, fill="cyan", width=6)

# Start updating functions
update_sensors()
update_display()
update_weather()
update_news()
# update_greeting()

root.mainloop()