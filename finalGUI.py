import tkinter as tk
from PIL import Image, ImageTk
import subprocess

# Create the main application window
root = tk.Tk()
root.title("AI Object Recognition App")             # Set window title
root.geometry("1366x768")                           # Set default window size
root.state("zoomed")                                # Open window in full screen
root.configure(bg="black")                          # Set background color to black

# Function to load and resize the background image based on the screen size
def update_bg():
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    bg_image = Image.open("extra/background.jpg")   # Load the background image
    bg_image = bg_image.resize((screen_width, screen_height))  # Resize to fit screen
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label.config(image=bg_photo)                 # Update label with new image
    bg_label.image = bg_photo                       # Keep a reference to avoid garbage collection

# Display the background image immediately on app start
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)   # Cover the whole window with the background
update_bg()                                         # Apply background image

# Title Label shown at the top center
title_label = tk.Label(
    root, 
    text="AI Object Recognition App", 
    font=("Arial", 32, "bold"), 
    fg="#00FFFF", 
    bg="black"
)
title_label.place(relx=0.5, y=50, anchor="center")  # Center horizontally, fixed vertical position

# Functions to handle hover effect on buttons
def on_enter(e):
    e.widget.config(bg="#00A3E0", relief="raised", fg="black")  # Change style on hover

def on_leave(e):
    e.widget.config(bg="#0077B6", relief="flat", fg="white")    # Revert style when not hovering

# Function to run a separate Python script when a button is clicked
def run_script(script_name):
    try:
        subprocess.run(["python", script_name], check=True)  # Safely run script
    except Exception as e:
        print(f"Error running {script_name}: {e}")            # Print any errors to the console

# List to store all created buttons (used for animation later)
buttons = []

# Function to create a styled button and add hover behavior
def create_button(text, y_pos, script_name, color):
    btn = tk.Button(
        root, text=text,
        font=("Arial", 18, "bold"),
        bg=color, fg="white", bd=3,
        padx=30, pady=15,
        relief="flat", activebackground="#555",
        command=lambda: run_script(script_name)  # When clicked, run the linked script
    )
    btn.place(x=100, y=y_pos, width=320, height=80)  # Place button at fixed position
    btn.bind("<Enter>", on_enter)                    # Hover effects
    btn.bind("<Leave>", on_leave)
    buttons.append(btn)                              # Add button to list for animation

# Create individual buttons with different colors and script actions
create_button("📸 Detect from Image", 150, "opt1(detectionfromimage).py", "#0077B6")
create_button("📹 Detect from Live Cam", 270, "opt2(livecamdetection).py", "#0088CC")
create_button("🎯 Detect Specific Object", 390, "opt3final(screenshot&video).py", "#00A3E0")
create_button("📂 View Detected Images", 510, "opt4(detectedscreenshot&video).py", "#00B4D8")

# Function to animate buttons sliding in from the left one-by-one
def slide_in(index=0):
    if index < len(buttons):
        btn = buttons[index]
        x_start = -350               # Starting x-position (off screen)
        x_end = 100                  # Final x-position
        step = 15                    # Pixels to move per frame

        def animate():
            nonlocal x_start
            if x_start < x_end:
                x_start += step
                btn.place(x=x_start, y=btn.winfo_y(), width=320, height=80)
                root.after(10, animate)  # Run again after 10 milliseconds
            else:
                btn.place(x=x_end, y=btn.winfo_y(), width=320, height=80)
                slide_in(index + 1)     # Animate the next button

        animate()  # Start animation for the current button

# Start button animation slightly after window loads
root.after(500, slide_in)

# Create "About The App" hyperlink-like label at the bottom center
about_label = tk.Label(
    root, 
    text="About The App", 
    fg="#FFD700", 
    bg="black", 
    font=("Arial", 16, "bold", "underline"), 
    cursor="hand2"
)
about_label.place(relx=0.5, y=700, anchor="center")  # Centered at the bottom

# Function to open the About section/script when label is clicked
def open_about():
    run_script("Abouttheapp.py")

about_label.bind("<Button-1>", lambda e: open_about())  # Bind left-click to function

# Run the application loop
root.mainloop()

