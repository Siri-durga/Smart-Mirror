import tkinter as tk
import tkinter.font as tkFont
import os

# Check if the font file exists
font_path = "fonts/Jersey15.ttf"
if not os.path.exists(font_path):
    print("?? Jersey15-Regular.ttf not found! Make sure it's in the same directory.")
    exit()

# Initialize Tkinter window
root = tk.Tk()
root.title("Jersey 15 Font Test")
root.geometry("400x200")
root.configure(bg="black")

# Load Jersey 15 font manually
custom_font = tkFont.Font(family="Jersey 15", size=30, weight="bold")
custom_font.configure(file=font_path)

# Create label using the font
label = tk.Label(root, text="Jersey 15 Test", font=custom_font, fg="white", bg="black")
label.pack(pady=50)

# Run Tkinter loop
root.mainloop()
