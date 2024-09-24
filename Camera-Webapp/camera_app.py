import streamlit as st
from PIL import Image

st.subheader("Color to Grayscale Converter")

with st.expander("Start Camera"):
    photo = st.camera_input("Camera")

with st.expander("Upload Image"):
    pc_photo = st.file_uploader("")

if photo:

    img = Image.open(photo)
    grey_img = img.convert("L")
    st.image(grey_img)

if pc_photo:

    img = Image.open(pc_photo)
    grey_img = img.convert("L")
    st.image(grey_img)

