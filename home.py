import streamlit as st
from moviepy.editor import VideoFileClip, concatenate_videoclips
import tempfile
import shutil

# Função para criar um vídeo reverso
def reverse_video(input_file, output_file):
    clip = VideoFileClip(input_file)
    reversed_clip = clip.fx(VideoFileClip.fx, lambda x: x.fl_time(-1))
    reversed_clip.write_videofile(output_file, codec='libx264')

# Função para cortar o vídeo
def crop_video(input_file, output_file, start_time, end_time):
    clip = VideoFileClip(input_file).subclip(start_time, end_time)
    clip.write_videofile(output_file, codec='libx264')

# Função para ajustar o brilho e o contraste do vídeo
def adjust_brightness_contrast(input_file, output_file, brightness, contrast):
    clip = VideoFileClip(input_file).fx(VideoFileClip.fx, lambda x: x.fx(VideoFileClip.fx, lambda y: y.set_brightness(brightness)))
    clip = clip.fx(VideoFileClip.fx, lambda x: x.fx(VideoFileClip.fx, lambda y: y.set_contrast(contrast)))
    clip.write_videofile(output_file, codec='libx264')

# Função para redimensionar o vídeo
def resize_video(input_file, output_file, width, height):
    clip = VideoFileClip(input_file).resize((width, height))
    clip.write_videofile(output_file, codec='libx264')

# Streamlit app
st.title("Manipulação de Vídeos MP4")
st.sidebar.header("Upload de Vídeo")

uploaded_file = st.sidebar.file_uploader("Escolha um arquivo de vídeo", type=["mp4"])

if uploaded_file is not None:
    # Get the uploaded file name
    input_video_filename = uploaded_file.name

    # Verifica se a biblioteca moviepy está instalada e a instala, caso não esteja
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        st.warning("A biblioteca moviepy não está instalada. Instalando a biblioteca...")

        from moviepy.editor import VideoFileClip

    # Realiza ações na barra lateral
    action = st.sidebar.selectbox("Selecione uma ação", ("Reverso", "Cortar", "Ajustar Brilho e Contraste", "Redimensionar"))

    if action == "Reverso":
        output_video_filename = "reversed_" + input_video_filename
        if st.button("Reverter Vídeo"):
            reverse_video(uploaded_file, output_video_filename)
            st.success("Vídeo revertido com sucesso!")
            with open(output_video_filename, "rb") as f:
                reversed_video = f.read()
            st.download_button("Clique aqui para baixar o vídeo revertido", data=reversed_video, file_name=output_video_filename, mime="video/mp4")

    elif action == "Cortar":
        start_time = st.sidebar.number_input("Tempo de Início (segundos)", value=0.0, step=1.0)
        end_time = st.sidebar.number_input("Tempo de Fim (segundos)", value=10.0, step=1.0)
        output_video_filename = "cropped_" + input_video_filename
        if st.button("Cortar Vídeo"):
            crop_video(uploaded_file, output_video_filename, start_time, end_time)
            st.success("Vídeo cortado com sucesso!")
            with open(output_video_filename, "rb") as f:
                cropped_video = f.read()
            st.download_button("Clique aqui para baixar o vídeo cortado", data=cropped_video, file_name=output_video_filename, mime="video/mp4")

    elif action == "Ajustar Brilho e Contraste":
        brightness = st.sidebar.slider("Brilho", -100, 100, 0, 1)
        contrast = st.sidebar.slider("Contraste", -100, 100, 0, 1)
        output_video_filename = "adjusted_" + input_video_filename
        if st.button("Ajustar Brilho e Contraste"):
            adjust_brightness_contrast(uploaded_file, output_video_filename, brightness, contrast)
            st.success("Brilho e contraste ajustados com sucesso!")
            with open(output_video_filename, "rb") as f:
                adjusted_video = f.read()
            st.download_button("Clique aqui para baixar o vídeo ajustado", data=adjusted_video, file_name=output_video_filename, mime="video/mp4")

    elif action == "Redimensionar":
        width = st.sidebar.number_input("Largura", value=640, step=10)
        height = st.sidebar.number_input("Altura", value=480, step=10)
        output_video_filename = "resized_" + input_video_filename
        if st.button("Redimensionar Vídeo"):
            resize_video(uploaded_file, output_video_filename, width, height)
            st.success("Vídeo redimensionado com sucesso!")
            with open(output_video_filename, "rb") as f:
                resized_video = f.read()
            st.download_button("Clique aqui para baixar o vídeo redimensionado", data=resized_video, file_name=output_video_filename, mime="video/mp4")

st.markdown("Powered by Cheetah Data Science")

