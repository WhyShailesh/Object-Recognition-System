Object Recognition System (YOLOv8)
This is a real-time Object Recognition System built using YOLOv8, Python, OpenCV, and PyTorch. It can detect objects in images, videos, and live camera feeds, and includes features like:
- Detect objects in images, videos, and live streams
- Automated screenshot capture when specific objects appear
- Automatic video recording during live detection
- Simple and user-friendly interface (Gradio/Streamlit option)

 Project Setup
1. Clone the Repository:
   git clone https://github.com/WhyShailesh/Object-Recognition-System.git
   cd Object-Recognition-System

2. Create a Virtual Environment (Recommended):
   Windows:
     python -m venv venv
     venv\Scripts\activate
   Linux/Mac:
     python3 -m venv venv
     source venv/bin/activate

3. Install Dependencies:
   pip install -r requirements.txt
   (If torch fails, check https://pytorch.org/get-started/locally/)

4. Download YOLOv8 Model:
   - By default, YOLO downloads automatically.
   - Or manually from: https://github.com/ultralytics/ultralytics

5. Run the Project:
   python app.py

 Features
- Image Detection: Upload an image and detect objects with bounding boxes
- Video Detection: Run detection on pre-recorded video files
- Live Camera Detection: Real-time detection from webcam
- Screenshot & Recording: Capture frames or record video automatically

 Tech Stack
Python 3.8+, YOLOv8 (Ultralytics), PyTorch, OpenCV, Gradio/Streamlit
 Common Issues & Fixes
- CUDA/GPU not found → Install CUDA toolkit and correct PyTorch version
- Slow detection → Runs faster with NVIDIA GPU
- Large files → Clear /outputs folder regularly
- Virtual environment errors → Activate venv before running

 Applications
Security, Surveillance, Traffic Monitoring, Industrial Automation, Retail, Smart Cities
 Future Scope
Multi-camera support, Cloud & IoT integration, Edge device optimization, Real-time alerts
 Author
Shailesh Biresh Yadav
📧 Email: ys06022000@gmail.com
🔗 LinkedIn: https://www.linkedin.com/in/shailesh0001/
🔗 GitHub: https://github.com/WhyShailesh
