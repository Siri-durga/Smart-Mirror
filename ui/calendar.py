import calendar
import tkinter as tk
from datetime import datetime

class CalendarApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Smart Mirror Calendar")
        self.master.configure(bg="black")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.header_label = tk.Label(master, font=("Helvetica", 18, "bold"), fg="white", bg="black")
        self.header_label.pack(pady=10)

        self.calendar_frame = tk.Frame(master, bg="black")
        self.calendar_frame.pack()

        self.button_frame = tk.Frame(master, bg="black")
        self.button_frame.pack(pady=10)

        self.prev_button = tk.Button(
            self.button_frame, text="Previous", font=("Helvetica", 14), command=self.previous_month, bg="gray", fg="white"
        )
        self.prev_button.pack(side="left", padx=10)

        self.next_button = tk.Button(
            self.button_frame, text="Next", font=("Helvetica", 14), command=self.next_month, bg="gray", fg="white"
        )
        self.next_button.pack(side="right", padx=10)

        self.show_calendar()

    def show_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Helvetica", 14, "bold"), fg="yellow", bg="black").grid(row=0, column=col, padx=5, pady=5)

        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        today = datetime.now().day if datetime.now().month == self.current_month and datetime.now().year == self.current_year else None

        for row_idx, week in enumerate(month_calendar, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    continue
                
                color = "white"
                if day == today:
                    color = "cyan"

                tk.Label(self.calendar_frame, text=str(day), font=("Helvetica", 14), fg=color, bg="black").grid(row=row_idx, column=col_idx, padx=10, pady=5)

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar()

    def previous_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar()


def get_calendar():
    calendar_window = tk.Toplevel()
    calendar_window.geometry("400x350")
    calendar_window.configure(bg="black")
    CalendarApp(calendar_window)

