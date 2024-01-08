import cv2
import numpy as np
import time
import os

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
moving_objects_folder = "moving_objects_frames"  # New folder for moving objects frames

# Threshold value for motion detection
threshold_value = 25

def process_frame(frame):
    global frame_counter, max_changes, max_changes_frame, min_changes, min_changes_frame, prev_frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    if frame_counter > 0:
        # Compute the absolute difference between the current and previous frame
        frame_delta = cv2.absdiff(blurred, prev_frame)

        # Apply a threshold to obtain a binary image
        threshold = cv2.threshold(frame_delta, threshold_value, 255, cv2.THRESH_BINARY)[1]

        # Perform dilation to fill in the holes
        dilated = cv2.dilate(threshold, None, iterations=2)

        # Find contours of the thresholded image
        contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Reset maximum changes if a new frame with more changes is found
        if len(contours) > max_changes:
            max_changes = len(contours)
            max_changes_frame = frame.copy()

        # Reset minimum changes if a new frame with fewer changes is found
        if len(contours) < min_changes:
            min_changes = len(contours)
            min_changes_frame = frame.copy()

        # Draw rectangles around the significant motion regions
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Save the frames of moving objects
            moving_object_frame = frame[y:y+h, x:x+w]
            moving_object_filename = os.path.join(moving_objects_folder, f"moving_object_{frame_counter}.jpg")
            cv2.imwrite(moving_object_filename, moving_object_frame)

    # Update the previous frame
    prev_frame = blurred.copy()

    # Save the frame
    frame_filename = os.path.join(output_folder, f"frame_{frame_counter}.jpg")
    cv2.imwrite(frame_filename, frame)

    # Increment frame counter
    frame_counter += 1

def on_threshold_change(value):
    global threshold_value
    threshold_value = value

# Create output folders if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(max_changes_folder, exist_ok=True)
os.makedirs(min_changes_folder, exist_ok=True)
os.makedirs(moving_objects_folder, exist_ok=True)  # Create moving objects folder

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

# Create a new window for the camera view
cv2.namedWindow("Camera View")

# Create a trackbar for threshold adjustment
cv2.createTrackbar("Threshold", "Camera View", threshold_value, 255, on_threshold_change)

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

    # Show the camera view in the window
    cv2.imshow("Camera View", frame)

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

# Print the total number of frames
print("Total number of frames:", frame_counter)

# Print the threshold value used
print("Threshold value:", threshold_value)

# Display the frame with the least frequent changes in a new window
if min_changes_frame is not None:
    cv2.imshow("Least Changes Frame", min_changes_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Display the frame with the most frequent changes in a new window
if max_changes_frame is not None:
    cv2.imshow("Most Changes Frame", max_changes_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Display the recorded video with arrow marks indicating changes
recorded_video = cv2.VideoCapture("recorded_video.mp4")
prev_frame = None

while True:
    ret, frame = recorded_video.read()

    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_frame is not None:
        # Compute the absolute difference between the current and previous frame
        frame_delta = cv2.absdiff(blurred, prev_frame)

        # Apply a threshold to obtain a binary image
        threshold = cv2.threshold(frame_delta, threshold_value, 255, cv2.THRESH_BINARY)[1]

        # Perform dilation to fill in the holes
        dilated = cv2.dilate(threshold, None, iterations=2)

        # Find contours of the thresholded image
        contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw arrows around the significant motion regions
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            arrow_start = (x + w // 2, y + h // 2)
            arrow_end = (x + w // 2 + 50, y + h // 2)
            cv2.arrowedLine(frame, arrow_start, arrow_end, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow("Recorded Video", frame)

    # Set the current frame as the previous frame for the next iteration
    prev_frame = blurred.copy()

    # Delay between frames (50 milliseconds)
    time.sleep(0.05)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the recorded video
recorded_video.release()

# Destroy all windows
cv2.destroyAllWindows()
