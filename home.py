import streamlit as st
import cv2
import numpy as np

# Function to create a reversed video and integrate it with the original video
def reverse_and_double_video(input_file, output_file):
    # Open the video file
    cap = cv2.VideoCapture(input_file)

    # Get video properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    fps = int(cap.get(5))

    # Create a VideoWriter object to save the reversed video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width * 2, frame_height * 2))

    # Read and write frames in reverse order
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    for frame in reversed(frames):
        # Double the size of the frame
        doubled_frame = cv2.resize(frame, (frame_width * 2, frame_height * 2))

        # Concatenate the original frame with the reversed frame
        combined_frame = np.concatenate((frame, doubled_frame), axis=1)

        out.write(combined_frame)

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

# Streamlit app
st.title("Reverse and Double Video Web App")
st.sidebar.header("Upload Video")
uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4"])

if uploaded_file is not None:
    # Get the uploaded file name
    input_video_filename = uploaded_file.name

    # Reverse the video, integrate with original, and save the combined video file
    output_video_filename = "reversed_and_doubled_" + input_video_filename
    reverse_and_double_video(input_video_filename, output_video_filename)

    # Display the original video
    st.subheader("Original Video")
    st.video(input_video_filename)

    # Display the reversed and doubled video
    st.subheader("Reversed and Doubled Video")
    st.video(output_video_filename)

st.markdown("Powered by Cheetah Data Science")
