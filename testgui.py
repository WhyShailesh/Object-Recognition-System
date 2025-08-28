import tkinter as tk
from PIL import Image, ImageTk, UnidentifiedImageError
import subprocess
import os

# Create main window
root = tk.Tk()
root.title("AI Object Recognition App")
root.geometry("1366x768")
root.state("zoomed")
root.configure(bg="black")  # Set background to black

# Background image paths (using absolute paths for reliability)
bg_image_dark = os.path.abspath("extra/background.jpg")
bg_image_light = os.path.abspath("extra/home2.jpg")

# Light bulb image paths
bulb_off_image = os.path.abspath("extra/bulb_off.png")
bulb_on_image = os.path.abspath("extra/bulb_on.png")

# Global variable to store background image reference
bg_photo = None

# Load and resize the background image dynamically
def update_bg(image_path, bg_color):
    global bg_photo  # Store reference to prevent garbage collection

    if not os.path.exists(image_path):  # Check if file exists
        print(f"Error: Image file '{image_path}' not found!")
        return

    try:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        bg_image = Image.open(image_path).resize((screen_width, screen_height))
        bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label.config(image=bg_photo, bg=bg_color)  # Change both image and background color

    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file '{image_path}'.")

# Background Label
bg_label = tk.Label(root, bd=0, highlightthickness=0, bg="black")  # Default to black
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
update_bg(bg_image_dark, "black")  # Default background

# Transparent text using a Label
title_label = tk.Label(root, text="AI Object Recognition App", 
                       font=("Arial", 32, "bold"), fg="#00FFFF", 
                       bd=0, highlightthickness=0, bg="black")
title_label.place(relx=0.5, y=50, anchor="center")

# Hover effect for buttons
def on_enter(e):
    e.widget.config(bg="#00A3E0", relief="raised", fg="black")

def on_leave(e):
    e.widget.config(bg="#0077B6", relief="flat", fg="white")

# Function to run a Python script
def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)
    except Exception as e:
        print(f"Error running {script_name}: {e}")

# Create buttons with modern style
buttons = []

def create_button(text, y_pos, script_name, color):
    btn = tk.Button(
        root, text=text,
        font=("Arial", 18, "bold"),
        bg=color, fg="white", bd=3,
        padx=30, pady=15,
        relief="flat", activebackground="#555",
        command=lambda: run_script(script_name)
    )
    btn.place(x=100, y=y_pos, width=320, height=80)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)

# Define buttons
create_button("📸 Track from Image", 150, "opt1(detectionfromimage).py", "#0077B6")
create_button("📹 Track from Live Cam", 270, "opt2(livecamdetection).py", "#0088CC")
create_button("🎯 Detect Specific Object", 390, "opt3final(screenshot&video).py", "#00A3E0")
create_button("📂 View Detected Images", 510, "opt4(detectedscreenshot&video).py", "#00B4D8")

# Slide-in animation for buttons
def slide_in(index=0):
    if index < len(buttons):
        btn = buttons[index]
        x_start = -350
        x_end = 100
        step = 15

        def animate():
            nonlocal x_start
            if x_start < x_end:
                x_start += step
                btn.place(x=x_start, y=btn.winfo_y(), width=320, height=80)
                root.after(10, animate)
            else:
                btn.place(x=x_end, y=btn.winfo_y(), width=320, height=80)
                slide_in(index + 1)  # Animate next button
        
        animate()

# Apply animations
root.after(500, slide_in)  # Delay button animation slightly

# "About The App" hyperlink (Fully Transparent)
about_label = tk.Label(root, text="About The App", fg="#FFD700", 
                       font=("Arial", 16, "bold", "underline"), cursor="hand2", 
                       bd=0, highlightthickness=0, bg="black")
about_label.place(relx=0.5, y=700, anchor="center")

def open_about():
    run_script("Abouttheapp.py")

about_label.bind("<Button-1>", lambda e: open_about())

# Light bulb functionality
def toggle_light():
    global is_light_on
    is_light_on = not is_light_on  # Toggle state

    if is_light_on:
        update_bg(bg_image_light, "white")  # Switch to light theme
        bulb_label.config(image=bulb_on_photo)
    else:
        update_bg(bg_image_dark, "black")  # Switch to dark theme
        bulb_label.config(image=bulb_off_photo)

# Load smaller bulb images (Ensure PNGs have transparent background!)
is_light_on = False  # Default state (off)
bulb_off_photo = ImageTk.PhotoImage(Image.open(bulb_off_image).resize((40, 55)))
bulb_on_photo = ImageTk.PhotoImage(Image.open(bulb_on_image).resize((40, 55)))

# Hanging light bulb button (Smaller, Moved Right, Transparent)
bulb_label = tk.Label(root, image=bulb_off_photo, cursor="hand2", bd=0, highlightthickness=0, bg="black")
bulb_label.place(relx=0.98, y=10, anchor="ne")  # Positioned towards right
bulb_label.bind("<Button-1>", lambda e: toggle_light())

# Run the application
root.mainloop()
