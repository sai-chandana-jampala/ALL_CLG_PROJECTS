import cv2
import numpy as np
import time
import os
import winsound
from flask import Flask, Response
import threading

# Global variables
frame_counter = 0
max_changes = 0
max_changes_frame = None
min_changes = float('inf')
min_changes_frame = None
prev_frame = None
output_folder = "captured_frames"
max_changes_folder = "most_changes_frames"
min_changes_folder = "least_changes_frames"
roi_folder = "roi_frames"
threshold_value = 25  # Initial threshold value
roi_start_point = None
roi_end_point = None
roi_selected = False

# Password settings
password = "hi"  # Change this to your desired password

# Buzz sound settings
frequency = 2500  # Frequency of the sound in Hz
duration = 1000  # Duration of the sound in milliseconds

# Create a Flask web application
app = Flask(__name__)

def process_frame(frame):
    global frame_counter, max_changes, max_changes_frame, min_changes, min_changes_frame, prev_frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    if frame_counter > 0:
        # Compute the absolute difference between the current and previous frame
        frame_delta = cv2.absdiff(blurred, prev_frame)

        # Apply the threshold to obtain a binary image
        _, threshold = cv2.threshold(frame_delta, threshold_value, 255, cv2.THRESH_BINARY)

        # Perform dilation to fill in the holes
        dilated = cv2.dilate(threshold, None, iterations=2)

        # Find contours of the thresholded image
        contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw arrows around the significant motion regions
        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.arrowedLine(frame, (x + w // 2, y + h // 2), (x + w // 2, y + h // 2), (0, 0, 255), 2)

        # Check for the frame with the most changes
        num_changes = len(contours)
        if num_changes > max_changes:
            max_changes = num_changes
            max_changes_frame = frame.copy()

        # Check for the frame with the least changes
        if num_changes < min_changes:
            min_changes = num_changes
            min_changes_frame = frame.copy()

    # Increment the frame counter
    frame_counter += 1

    # Update the previous frame
    prev_frame = blurred

def select_roi(event, x, y, flags, param):
    global roi_start_point, roi_end_point, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        roi_start_point = (x, y)
        roi_selected = False

    elif event == cv2.EVENT_LBUTTONUP:
        roi_end_point = (x, y)
        roi_selected = True

def play_beep_sound():
    duration_ms = 2 * 60 * 1000  # 2 minutes in milliseconds
    while True:
        winsound.Beep(frequency, duration)
        time.sleep(0.5)  # Delay between beeps

@app.route('/')
def index():
    return "Live Video Streaming"

def generate_frames():
    while True:
        # Read the current frame
        ret, frame = camera.read()

        if not ret:
            break

        # Process the frame
        process_frame(frame)

        # Convert the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield the frame in a byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def ask_password():
    entered_password = input("Enter the password: ")
    return entered_password == password

# Prompt for password
if ask_password():
    # Create output folders if they don't exist
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(max_changes_folder, exist_ok=True)
    os.makedirs(min_changes_folder, exist_ok=True)
    os.makedirs(roi_folder, exist_ok=True)

    # Determine the number of connected cameras
    num_cameras = 0
    while True:
        cap = cv2.VideoCapture(num_cameras)
        if not cap.read()[0]:
            break
        num_cameras += 1
        cap.release()

    # Use the last connected camera as the video source
    camera = cv2.VideoCapture(num_cameras - 1)

    # Start time
    start_time = time.time()

    # Create a VideoWriter object to record the video
    video_writer = cv2.VideoWriter("recorded_video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 30, (640, 480))

    # Create a window to adjust the motion detection threshold
    cv2.namedWindow("Threshold Adjustment")
    cv2.createTrackbar("Threshold", "Threshold Adjustment", threshold_value, 255, lambda x: None)

    # Create a window to select the ROI
    cv2.namedWindow("Camera View")
    cv2.setMouseCallback("Camera View", select_roi)

    @app.route('/video_feed')
    def video_feed():
        return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    # Start the Flask application
    app.run(host='192.168.218.251', port=5000)

    while True:
        # Read the current frame
        ret, frame = camera.read()

        # Stop if no frame is captured or after 10 seconds
        if not ret or time.time() - start_time > 10:
            break

        # Process the frame
        process_frame(frame)

        # Write the frame to the video file
        video_writer.write(frame)

        # Show the camera view in a new window
        cv2.imshow("Camera View", frame)

        # Draw the ROI selection rectangle if ROI is selected
        if roi_selected and roi_start_point is not None and roi_end_point is not None:
            cv2.rectangle(frame, roi_start_point, roi_end_point, (0, 255, 0), 2)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    camera.release()

    # Release the video writer
    video_writer.release()

    # Save the frames with the most and least frequent changes
    if max_changes_frame is not None:
        max_changes_filename = os.path.join(max_changes_folder, "most_changes_frame.jpg")
        cv2.imwrite(max_changes_filename, max_changes_frame)

    if min_changes_frame is not None:
        min_changes_filename = os.path.join(min_changes_folder, "least_changes_frame.jpg")
        cv2.imwrite(min_changes_filename, min_changes_frame)

    # Save the ROI frame
    if roi_selected and roi_start_point is not None and roi_end_point is not None:
        roi_frame = frame[roi_start_point[1]:roi_end_point[1], roi_start_point[0]:roi_end_point[0]]
        roi_filename = os.path.join(roi_folder, "roi_frame.jpg")
        cv2.imwrite(roi_filename, roi_frame)

    # Display the frame with the most and least frequent changes
    if max_changes_frame is not None:
        cv2.imshow("Most Changes", max_changes_frame)

    if min_changes_frame is not None:
        cv2.imshow("Least Changes", min_changes_frame)

    # Close all windows
    cv2.destroyAllWindows()

else:
    print("Incorrect password. Access denied.")
    play_beep_sound()

#http://localhost:5000/video_feed
# http://localhost:5000/
