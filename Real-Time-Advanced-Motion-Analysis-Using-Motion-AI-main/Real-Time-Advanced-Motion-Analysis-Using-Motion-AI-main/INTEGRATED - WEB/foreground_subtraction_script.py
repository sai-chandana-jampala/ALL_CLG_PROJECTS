
import cv2
import numpy as np
from pydmd import DMD
import sys
import os  # Import the os module for path operations

def remove_background_dmd(video_path, output_path):
    # Read video
    cap = cv2.VideoCapture(video_path)

    # Read frames
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    # Convert frames to a NumPy array
    video_data = np.array(frames)

    # Reshape video data to 2D (space x time)
    video_data = video_data.reshape(video_data.shape[0], -1).T

    # Dynamic Mode Decomposition
    dmd = DMD(svd_rank=2)  # You can adjust svd_rank based on your data
    dmd.fit(video_data)

    # Reconstruct background
    background = np.real(dmd.modes[:, 0]).reshape(-1, 1)

    # Subtract background from original video data
    foreground = video_data - background

    # Reshape the foreground to the original shape
    foreground = foreground.T.reshape(video_data.shape[1], *frames[0].shape)

    # Ensure the output folder exists
    os.makedirs(output_path, exist_ok=True)

    # Save the result
    output_file = os.path.join(output_path, 'foreground.mp4')  # Use os.path.join for correct path construction
    out = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), (foreground.shape[2], foreground.shape[1]))

    for frame in foreground:
        # Convert frame data type to uint8
        frame = frame.astype(np.uint8)
        out.write(frame)

    out.release()

    # Release video capture
    cap.release()

    print(f"Foreground video saved at: {output_file}")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python foreground_subtraction_script.py <input_video_path> <output_folder>")
        sys.exit(1)

    # Get the input video path and output folder from command-line arguments
    input_video_path = sys.argv[1]
    output_folder = sys.argv[2]

    remove_background_dmd(input_video_path, output_folder)
