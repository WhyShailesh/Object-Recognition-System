import tkinter as tk
from tkinter import Canvas

class ObjectRecognitionApp:
    def __init__(self, root):
        # Configure the main window
        self.root = root
        self.root.title("About Object Recognition System")
        self.root.attributes('-fullscreen', True)  # Launch in full-screen
        self.root.configure(bg="#1E1E1E")  # Dark background color

        # Create background with gradient effect
        self.create_gradient_background()

        # Title Label - Displayed at the top left
        title = tk.Label(root, text="Object Detection System using YOLOv8",
                         font=("Arial", 28, "bold"), fg="#00FFF5", bg="#1E1E1E", anchor="w", justify="left")
        title.place(x=50, y=30)

        # Features section with a bullet list
        features = [
            "✓ Detects objects in images, videos, and live camera feeds.",
            "✓ Supports automatic screenshot capture for specific objects.",
            "✓ Records video when specific objects are detected.",
            "✓ Real-time object detection with high accuracy.",
            "✓ User-friendly interface with smooth animations."
        ]
        self.create_section("🌟 Features", features, y_offset=100)

        # Technologies used section
        technologies = [
            "🔹 YOLOv8 for object detection",
            "🔹 OpenCV for image and video processing",
            "🔹 Python for backend development"
        ]
        self.create_section("🛠️ Technologies Used", technologies, y_offset=350)

        # Applications section
        applications = [
            "🔍 Security & Surveillance",
            "🚦 Traffic Monitoring",
            "🏭 Industrial Automation",
            "🏬 Retail & Inventory Management",
            "🏙️ Smart City Applications"
        ]
        self.create_section("📌 Applications", applications, y_offset=600)

        # Create an Exit button at the bottom-right corner
        self.exit_btn = tk.Button(root, text="Exit", font=("Arial", 18, "bold"), fg="white", bg="#FF1744",
                                  activebackground="#D50000", activeforeground="white",
                                  command=root.destroy, padx=30, pady=10, relief="flat", borderwidth=0)

        # Position the Exit button using screen width for bottom-right alignment
        screen_width = self.root.winfo_screenwidth()
        self.exit_btn.place(x=screen_width - 150, y=800)

        # Hover effect for Exit button
        self.exit_btn.bind("<Enter>", lambda e: self.exit_btn.config(bg="#D50000"))
        self.exit_btn.bind("<Leave>", lambda e: self.exit_btn.config(bg="#FF1744"))

    def create_section(self, title, items, y_offset):
        """Creates a section with a title and a list of bullet point labels."""
        # Section title
        section_title = tk.Label(self.root, text=title, font=("Arial", 20, "bold"), fg="#FFD700", bg="#1E1E1E",
                                 anchor="w", justify="left")
        section_title.place(x=50, y=y_offset)

        # Add bullet items below the section title
        for i, item in enumerate(items):
            label = tk.Label(self.root, text=item, font=("Arial", 16), fg="white", bg="#1E1E1E",
                             anchor="w", justify="left")
            label.place(x=70, y=y_offset + 40 + (i * 30))  # Adjust vertical spacing

    def create_gradient_background(self):
        """Draws a vertical gradient background using a Canvas."""
        canvas = Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        canvas.place(x=0, y=0)

        # Draw rectangles from top to bottom to simulate a gradient effect
        for i in range(100):
            gray_value = 30 + i  # Vary the gray shade gradually
            hex_color = f"#{gray_value:02X}{gray_value:02X}{gray_value:02X}"
            canvas.create_rectangle(0, i * 10, self.root.winfo_screenwidth(), (i + 1) * 10, fill=hex_color, outline=hex_color)

# Create and run the GUI application
root = tk.Tk()
app = ObjectRecognitionApp(root)
root.mainloop()
