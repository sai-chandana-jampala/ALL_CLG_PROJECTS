# video_compression.py

import os  # Operating system module
import sys  # System-specific parameters and functions
import cv2  # OpenCV library for computer vision
import numpy as np  # Numerical computing library
from pydmd import DMD  # Dynamic Mode Decomposition library

# Function to extract frames from a video
def video_to_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()
    return frames

# Function to convert frames to a video
def frames_to_video(frames, output_path):
    height, width, layers = frames[0].shape
    size = (width, height)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, size)

    for frame in frames:
        out.write(frame)

    out.release()

# Function to calculate Peak Signal-to-Noise Ratio (PSNR)
def calculate_psnr(original_video, reconstructed_video):
    mse = np.mean((original_video - reconstructed_video) ** 2)
    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr

# Function to get the size of a video file
def get_video_size(video_path):
    return os.path.getsize(video_path)

# Function for DMD-based video compression
def dmd_video_compression(input_video_path, output_video_path, rank=None):
    frames = video_to_frames(input_video_path)

    # Print the size of the original video
    original_size = get_video_size(input_video_path)
    print(f"Original video size: {original_size / (1024 * 1024):.2f} MB")

    # Convert frames to a 3D array (height, width, time)
    X = np.array(frames).reshape(-1, frames[0].shape[0] * frames[0].shape[1] * frames[0].shape[2])

    # Perform DMD
    dmd = DMD(svd_rank=5)
    dmd.fit(X.T)

    # Reconstruct the video
    reconstructed_frames = dmd.modes @ dmd.dynamics

    # Reshape and normalize
    reconstructed_frames = reconstructed_frames.real.T.reshape((-1,) + frames[0].shape)
    reconstructed_frames = np.clip(reconstructed_frames, 0, 255).astype(np.uint8)

    # Calculate PSNR between original and reconstructed videos
    psnr_value = calculate_psnr(np.array(frames), reconstructed_frames)
    print(f"PSNR between original and reconstructed videos: {psnr_value:.2f} dB")

    # Save the compressed video with the correct file extension
    compressed_video_path = output_video_path
    frames_to_video(reconstructed_frames, compressed_video_path)

    # Print the size of the compressed video
    compressed_size = get_video_size(compressed_video_path)
    print(f"Compressed video size: {compressed_size / (1024 * 1024):.2f} MB")

# Get the input and output video paths from command-line arguments
input_video_path = sys.argv[1]
output_video_path = sys.argv[2]
rank = int(sys.argv[3]) if sys.argv[3].isdigit() else None

# Call the compression function with the provided arguments
dmd_video_compression(input_video_path, output_video_path, rank)
