import streamlit as st
from moviepy.editor import VideoFileClip

# Function to create a reversed video
def reverse_video(input_file, output_file):
    clip = VideoFileClip(input_file)
    reversed_clip = clip.fx(VideoFileClip.fx, lambda x: x.fl_time(-1))
    reversed_clip.write_videofile(output_file, codec='libx264')

# Streamlit app
st.title("Reverse Video Web App")
st.sidebar.header("Upload Video")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo de vídeo", type=["mp4"])

if uploaded_file is not None:
    # Get the uploaded file name
    input_video_filename = uploaded_file.name

    # Reverse the video and save the reversed video file
    output_video_filename = "reversed_" + input_video_filename
    reverse_video(uploaded_file, output_video_filename)

    # Display the original video
    st.subheader("Vídeo Original")
    st.video(uploaded_file)

    # Display the reversed video
    st.subheader("Vídeo Revertido")
    st.video(output_video_filename)

    # Offer the reversed video for download
    st.subheader("Download Vídeo Revertido")
    with open(output_video_filename, "rb") as f:
        reversed_video = f.read()
    st.download_button("Clique aqui para baixar o vídeo revertido", data=reversed_video, file_name=output_video_filename, mime="video/mp4")

st.markdown("Powered by Cheetah Data Science")

