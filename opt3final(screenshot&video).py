import cv2
from ultralytics import YOLO
import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from PIL import Image, ImageTk
import time


# Load the YOLOv8 model (nano version)
model = YOLO('yolov8n.pt')

# Get list of all detectable object names 
object_names = list(model.names.values())

# Format object names for displaying as tooltip text in the GUI
def format_tooltip_text(names, objects_per_line=5):
    lines = []
    for i in range(0, len(names), objects_per_line):
        lines.append(', '.join(names[i:i + objects_per_line]))
    return '\n'.join(lines)

tooltip_text = format_tooltip_text(object_names)



# Define absolute paths to save screenshots and videos
screenshot_folder = os.path.abspath("saved_screenshot")
video_folder = os.path.abspath("saved_video")

# Create the folders if they don't exist
os.makedirs(screenshot_folder, exist_ok=True)
os.makedirs(video_folder, exist_ok=True)



def open_camera(action, object_name):
    """
    This function captures live webcam video,
    detects the specified object using YOLOv8,
    and performs screenshot or video capture depending on 'action'.
    """
    webcamera = cv2.VideoCapture(0)
    exit_button_pressed = False
    object_in_frame = False  # Avoid repeating screenshots
    recording = False
    video_writer = None
    video_start_time = 0  
    recording_end_time = 0

    # Mouse click handler for detecting custom "Exit" button click
    def mouse_callback(event, x, y, flags, param):
        nonlocal exit_button_pressed
        if event == cv2.EVENT_LBUTTONDOWN:
            if 20 <= x <= 120 and frame.shape[0] - 70 <= y <= frame.shape[0] - 20:
                print("Exit button clicked, closing camera window...")
                exit_button_pressed = True

    cv2.namedWindow("Live Detection", cv2.WINDOW_NORMAL)

    while True:
        success, frame = webcamera.read()
        if not success:
            break

        cv2.setMouseCallback("Live Detection", mouse_callback)

        # Run YOLO object detection
        results = model(frame)
        detected = False

        # Loop through results to check for target object
        for result in results:
            frame = result.plot()  # Draw bounding boxes
            for box in result.boxes:
                detected_class = model.names[int(box.cls[0])]
                confidence = box.conf[0].item()
                if detected_class.lower() == object_name.lower() and confidence > 0.6:
                    detected = True
                    break

        # Draw a red rectangle for the custom "Exit" button
        cv2.rectangle(frame, (20, frame.shape[0] - 70), (120, frame.shape[0] - 20), (0, 0, 255), -1)
        cv2.putText(frame, "Exit", (40, frame.shape[0] - 35), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)

        cv2.imshow("Live Detection", frame)

        # If object is detected and screenshot is selected
        if detected:
            if action == "screenshot" and not object_in_frame:
                screenshot_path = os.path.join(
                    screenshot_folder, f"screenshot_{object_name}_{len(os.listdir(screenshot_folder))}.jpg")
                if cv2.imwrite(screenshot_path, frame):
                    print(f"Screenshot saved at {screenshot_path}")
                else:
                    print("Failed to save screenshot!")
                object_in_frame = True

            # If object is detected and video is selected
            elif action == "video" and not recording:
                video_path = os.path.join(
                    video_folder, f"video_{object_name}_{len(os.listdir(video_folder))}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))
                recording = True
                video_start_time = time.time()
                recording_end_time = video_start_time + 5
                print("Recording video for at least 5 seconds...")

        # Write video frames if recording
        if recording and video_writer:
            video_writer.write(frame)

        # Stop recording after 5 seconds
        if recording and time.time() >= recording_end_time:
            print("5 seconds passed, stopping video recording.")
            recording = False
            video_writer.release()
            video_writer = None

        # Reset flag if object is no longer detected
        if not detected:
            object_in_frame = False

        if exit_button_pressed:
            break

        # Press 'q' key to manually exit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    # Cleanup on exit
    if recording and video_writer:
        video_writer.release()
    webcamera.release()
    cv2.destroyWindow("Live Detection")



def start_gui():
    root = tk.Tk()
    root.state("zoomed")
    root.title("Object Detector")

    # Load and display background image
    bg_image = Image.open("extra/opt2bg.jpg")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    # Frame to hold input and buttons
    frame = tk.Frame(root, bg='black')
    frame.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

    # Label and Entry to input object name
    label = tk.Label(frame, text="Enter object name:", font=("Arial", 20), fg="white", bg="black")
    label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    object_name_entry = tk.Entry(frame, font=("Arial", 20), width=30)
    object_name_entry.grid(row=0, column=1, padx=10, pady=10)

    # Info ("i.e") button to show detectable object list
    info_button = tk.Button(frame, text="i.e", font=("Arial", 18), bg="black", fg="white", activebackground="gray", activeforeground="white")
    info_button.grid(row=0, column=2, padx=10, pady=10)

    # Tooltip window that shows detectable object names
    def show_tooltip(event):
        tooltip = tk.Toplevel(root)
        tooltip.wm_overrideredirect(True)
        tooltip.geometry(f"500x300+{info_button.winfo_rootx()}+{info_button.winfo_rooty()+30}")
        tooltip.configure(bg="black")

        text_widget = scrolledtext.ScrolledText(tooltip, wrap=tk.WORD, width=60, height=15, font=("Arial", 14), bg="black", fg="white")
        text_widget.insert(tk.END, tooltip_text)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)

        def hide_tooltip(event):
            tooltip.destroy()

        tooltip.bind("<Leave>", hide_tooltip)

    info_button.bind("<Enter>", show_tooltip)

    # Frame for action buttons
    button_frame = tk.Frame(frame, bg='black')
    button_frame.grid(row=2, column=0, columnspan=3, pady=40)

    # Hover effect functions
    def on_hover(button):
        button.config(bg="gray", fg="white")

    def on_leave(button):
        button.config(bg="black", fg="white")

    # Screenshot button
    screenshot_button = tk.Button(
        button_frame, text="Screenshot", font=("Arial", 18),
        bg="black", fg="white", activebackground="gray", activeforeground="white",
        command=lambda: open_camera("screenshot", object_name_entry.get())
    )
    screenshot_button.pack(side=tk.LEFT, padx=50)

    # Video button
    video_button = tk.Button(
        button_frame, text="Take Video", font=("Arial", 18),
        bg="black", fg="white", activebackground="gray", activeforeground="white",
        command=lambda: open_camera("video", object_name_entry.get())
    )
    video_button.pack(side=tk.LEFT, padx=50)

    # Bind hover effects to buttons
    for button in [screenshot_button, video_button]:
        button.bind("<Enter>", lambda e, b=button: on_hover(b))
        button.bind("<Leave>", lambda e, b=button: on_leave(b))

    root.mainloop()

start_gui()
