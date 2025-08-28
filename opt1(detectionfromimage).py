import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from ultralytics import YOLO  

# Load the pre-trained YOLOv8 model 
model = YOLO('yolov8n.pt')

def upload_and_detect():
    """ 
    Opens a file dialog to select an image, runs YOLOv8 detection on it,
    and displays the image with detected objects.
    """
    # Open file selection dialog for image files
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    
    if not file_path:
        print("No file selected")  # If user cancels the dialog
        return
    
    # Read the selected image using OpenCV
    image = cv2.imread(file_path)
    
    # Run object detection on the image
    results = model(image)
    
    # Draw detection results on the image 
    detected_image = results[0].plot()

    # Resize image to fit nicely in the display window
    screen_width = 800
    screen_height = 600
    detected_image_resized = cv2.resize(detected_image, (screen_width, screen_height))

    # Show the detected image in a pop-up window
    cv2.imshow("Detected Objects", detected_image_resized)

    # Wait for a key press, then close the image window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Create main application window
root = tk.Tk()
root.title("YOLOv8 Object Detection")    # Window title
root.state('zoomed')                     # Open in full screen mode

# Load and resize a background image to match the screen size
bg_image = Image.open("extra/opt1bg.jpg")
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
bg_photo = ImageTk.PhotoImage(bg_image)

# Display the background image using a Label
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the window

# Title/Instruction Label (centered at 30% of screen height)
tk.Label(
    root,
    text="Upload an image for object detection",
    font=("Arial", 20, "bold"),
    fg="white",
    bg="black"
).place(relx=0.5, rely=0.3, anchor="center")

# Upload Button (centered at 50% height)
btn_upload = tk.Button(
    root,
    text="\U0001F4C2 Upload Image",         # Folder emoji
    command=upload_and_detect,              # Runs detection on click
    font=("Arial", 16, "bold"),
    bg="blue", fg="white",
    padx=30, pady=15                        # Padding for nice button size
)
btn_upload.place(relx=0.5, rely=0.5, anchor="center")

# Start the GUI loop
root.mainloop()
