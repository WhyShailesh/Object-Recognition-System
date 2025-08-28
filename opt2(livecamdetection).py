import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO('yolov8n.pt')

# Open webcam
webcamera = cv2.VideoCapture(0)

# Get video feed dimensions
frame_width = int(webcamera.get(3))  # Get frame width
frame_height = int(webcamera.get(4))  # Get frame height

# Define button position (bottom-right corner)
exit_button_w, exit_button_h = 60, 30  # Smaller button size
exit_button_x = frame_width - exit_button_w - 20  # 20px margin from right
exit_button_y = frame_height - exit_button_h - 20  # 20px margin from bottom

def click_event(event, x, y, flags, param):
    """ Callback function to detect clicks on the exit button. """
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
        if exit_button_x <= x <= exit_button_x + exit_button_w and exit_button_y <= y <= exit_button_y + exit_button_h:
            print("Exit button clicked. Closing program.")
            running = False  # Stop the loop

# Create a named window and set mouse callback
cv2.namedWindow("Live Camera")
cv2.setMouseCallback("Live Camera", click_event)

running = True  # Flag to control the loop
while running:
    success, frame = webcamera.read()
    if not success:
        break

    # Run YOLO detection
    results = model.track(frame, conf=0.8, imgsz=480)

    # Draw the exit button (bottom-right)
    cv2.rectangle(frame, (exit_button_x, exit_button_y), 
                  (exit_button_x + exit_button_w, exit_button_y + exit_button_h), (0, 0, 255), -1)
    cv2.putText(frame, "EXIT", (exit_button_x + 10, exit_button_y + 20), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Display detections and button
    cv2.putText(frame, f"Total: {len(results[0].boxes)}", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Live Camera", results[0].plot())

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
webcamera.release()
cv2.destroyAllWindows()
