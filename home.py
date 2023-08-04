import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile
import shutil

# Function to create a reversed video and integrate it with the original video
def reverse_and_double_video(input_file, output_file):
    clip = VideoFileClip(input_file)
    reversed_clip = clip.fx(VideoFileClip.fx, lambda x: x.fl_time(-1))
    final_clip = concatenate_videoclips([clip, reversed_clip.resize(2.0)])

    final_clip.write_videofile(output_file, codec='libx264')

# Streamlit app
st.title("Reverse and Double Video Web App")
st.sidebar.header("Upload Video")
uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4"])

if uploaded_file is not None:
    # Get the uploaded file name
    input_video_filename = uploaded_file.name

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_filename = temp_file.name
        shutil.copyfileobj(uploaded_file, temp_file)

    # Reverse the video, integrate with original, and save the combined video file
    output_video_filename = "reversed_and_doubled_" + input_video_filename
    reverse_and_double_video(temp_filename, output_video_filename)

    # Display the original video
    st.subheader("Original Video")
    st.video(uploaded_file)

    # Display the reversed and doubled video
    st.subheader("Reversed and Doubled Video")
    with open(output_video_filename, "rb") as f:
        reversed_doubled_video = f.read()
    st.video(reversed_doubled_video)

st.markdown("Powered by Cheetah Data Science")
