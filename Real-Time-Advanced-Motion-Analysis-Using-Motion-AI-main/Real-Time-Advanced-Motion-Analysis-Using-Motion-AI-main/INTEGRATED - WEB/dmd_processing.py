import cv2
import os
import numpy as np
from pydmd import DMD  # Import DMD library for dynamic mode decomposition
import sys

def dmd_object_tracking(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return None, None, None

    # Read the first frame from the video
    _, frame1 = cap.read()
    # Convert the first frame to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # Initialize variables
    frame_count = 0
    frequency_dict = {}

    # Create an output video file
    output_video_path = os.path.join(output_folder, 'output.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, 30.0, (frame1.shape[1], frame1.shape[0]))

    # Loop through each frame of the video
    while True:
        # Read the next frame
        ret, frame2 = cap.read()
        if not ret:
            break

        # Convert the current frame to grayscale
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        # Calculate the absolute difference between consecutive frames
        frame_diff = cv2.absdiff(gray1, gray2)

        try:
            # Apply Dynamic Mode Decomposition (DMD) on the frame difference
            dmd = DMD(svd_rank=5)
            dmd.fit(frame_diff)
            background = dmd.modes @ dmd.dynamics
            diff_background = np.abs(frame_diff - background).astype(np.uint8)

            # Threshold the difference to get binary foreground
            _, thresh = cv2.threshold(diff_background, 30, 255, cv2.THRESH_BINARY)
            # Find contours in the binary image
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Loop through the contours and identify regions of interest (ROI)
            for contour in contours:
                if cv2.contourArea(contour) > 1000:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frequency_dict[frame_count] = frequency_dict.get(frame_count, 0) + 1

            # Save the current frame as an image
            if not frame2.size == 0:
                most_frequent_frame_path = os.path.join(output_folder, f'most_frequent_frame_{frame_count}.png')
                least_frequent_frame_path = os.path.join(output_folder, f'least_frequent_frame_{frame_count}.png')

                cv2.imwrite(most_frequent_frame_path, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
                cv2.imwrite(least_frequent_frame_path, cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))

            # Write the frame to the output video
            out.write(frame2)
            frame_count += 1

        except Exception as e:
            print(f"Error processing frame {frame_count}: {e}")

        # Check for the 'Esc' key to exit the loop
        if cv2.waitKey(30) & 0xFF == 27:
            break

    # Release resources
    out.release()
    cap.release()
    cv2.destroyAllWindows()

    # Find the most and least frequently changed frames
    most_frequent_frame = max(frequency_dict, key=frequency_dict.get, default=None)
    least_frequent_frame = min(frequency_dict, key=frequency_dict.get, default=None)

    # Print the results
    if most_frequent_frame is not None and least_frequent_frame is not None:
        print(f"The most frequently changed frame is: frame_{most_frequent_frame}.png")
        print(f"The least frequently changed frame is: frame_{least_frequent_frame}.png")

    return output_video_path, most_frequent_frame_path, least_frequent_frame_path

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python dmd_processing.py <video_path> <output_folder>")
        sys.exit(1)

    # Get the video path and output folder from command-line arguments
    video_path = sys.argv[1]
    output_folder = sys.argv[2]

    # Create the output folder if it does not exist
    os.makedirs(output_folder, exist_ok=True)

    # Call the function for DMD-based object tracking
    dmd_object_tracking(video_path, output_folder)
