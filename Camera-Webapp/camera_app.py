import streamlit as st
from PIL import Image

with st.expander("Start Camera"):
    photo = st.camera_input("Camera")

if photo:

    img = Image.open(photo)
    grey_img = img.convert("L")
    st.image(grey_img)
