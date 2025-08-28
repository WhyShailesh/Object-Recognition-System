import os
import cv2
import tkinter as tk
from tkinter import Label, Menu, messagebox, Frame, Canvas
from PIL import Image, ImageTk

# Define folder paths for saved screenshots and videos
screenshot_folder = "saved_screenshot"
video_folder = "saved_video"

# Create the main GUI window
root = tk.Tk()
root.title("Detected Objects Viewer")
root.state("zoomed")  # Launch in maximized mode
root.configure(bg="black")
root.resizable(True, True)

# Used to hold references to images so they are not garbage collected
image_references = []

def open_image(image_path):
    """Opens an image using OpenCV when the image thumbnail is clicked."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Unable to open image {image_path}")
        return
    cv2.imshow("Image Viewer", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def play_video(video_path):
    """Plays a video using OpenCV when a video button is clicked."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video {video_path}")
        return
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video Player", frame)
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q') or cv2.getWindowProperty("Video Player", cv2.WND_PROP_VISIBLE) < 1:
            break
    cap.release()
    cv2.destroyAllWindows()

def delete_file(file_path, widget):
    """Deletes a selected file after confirmation and removes it from the UI."""
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {os.path.basename(file_path)}?")
    if confirm:
        try:
            os.remove(file_path)
            widget.destroy()
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

def show_context_menu(event, file_path, widget):
    """Displays a right-click context menu with a 'Delete' option."""
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Delete", command=lambda: delete_file(file_path, widget))
    menu.post(event.x_root, event.y_root)

# Horizontal and vertical mouse scroll functions
def on_mouse_wheel_horizontal(event, canvas):
    canvas.xview_scroll(-1 * (event.delta // 120), "units")

def on_mouse_wheel_vertical(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

# Create a horizontally scrollable frame for images
def create_horizontal_scrollable_frame(parent):
    outer_frame = Frame(parent, bg="black")
    canvas = Canvas(outer_frame, bg="black", highlightthickness=0)
    frame = Frame(canvas, bg="black")
    canvas.configure(xscrollcommand=None)  # No scrollbar
    canvas.pack(side="top", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel_horizontal(event, canvas)))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    outer_frame.pack(fill="both", expand=True)
    return frame

# Create a vertically scrollable frame for videos
def create_vertical_scrollable_frame(parent):
    outer_frame = Frame(parent, bg="black")
    canvas = Canvas(outer_frame, bg="black", highlightthickness=0)
    frame = Frame(canvas, bg="black")
    canvas.configure(yscrollcommand=None)
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: on_mouse_wheel_vertical(event, canvas)))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
    outer_frame.pack(fill="both", expand=True)
    return frame

def load_images():
    """Loads all image thumbnails from the screenshot folder."""
    global image_references
    image_references.clear()  # Reset references
    for widget in frame_images.winfo_children():
        widget.destroy()

    if not os.path.exists(screenshot_folder):
        return

    image_files = [f for f in os.listdir(screenshot_folder) if f.endswith((".jpg", ".png", ".jpeg"))]
    for img_file in image_files:
        img_path = os.path.join(screenshot_folder, img_file)
        try:
            img = Image.open(img_path)
            img.thumbnail((200, 200))  # Resize for thumbnail display
            img_tk = ImageTk.PhotoImage(img)
            image_references.append(img_tk)
            label = Label(frame_images, image=img_tk, cursor="hand2", bg="black")
            label.pack(side="left", padx=5, pady=1)
            label.bind("<Button-1>", lambda e, p=img_path: open_image(p))  # Left-click to open
            label.bind("<Button-3>", lambda e, p=img_path, w=label: show_context_menu(e, p, w))  # Right-click for delete
        except Exception as e:
            print(f"Error loading image {img_file}: {e}")

def load_videos():
    """Loads all video files and creates buttons to play them."""
    for widget in frame_videos.winfo_children():
        widget.destroy()

    if not os.path.exists(video_folder):
        return

    video_files = [f for f in os.listdir(video_folder) if f.endswith((".mp4", ".avi", ".mov"))]
    for vid_file in video_files:
        vid_path = os.path.join(video_folder, vid_file)
        btn = tk.Button(frame_videos, text=vid_file, command=lambda p=vid_path: play_video(p), bg="#444", fg="white")
        btn.pack(pady=5, fill="x")

# Create title label at the top
title_label = tk.Label(root, text="Detected Objects Viewer", font=("Arial", 24, "bold"), fg="white", bg="black")
title_label.pack(pady=10)

# Section for screenshots
label_screenshot = tk.Label(root, text="Saved Screenshots", font=("Arial", 18, "bold"), fg="white", bg="black")
label_screenshot.pack()
frame_images = create_horizontal_scrollable_frame(root)

# Section for videos
label_video = tk.Label(root, text="Saved Videos", font=("Arial", 18, "bold"), fg="white", bg="black")
label_video.pack(fill="both")
frame_videos = create_vertical_scrollable_frame(root)

# Refresh button to reload images and videos
btn_refresh = tk.Button(root, text="Refresh", command=lambda: [load_images(), load_videos()], bg="red", fg="white")
btn_refresh.pack(side="bottom", pady=10)

# Load initial images and videos on launch
load_images()
load_videos()

# Start the Tkinter event loop
root.mainloop()
