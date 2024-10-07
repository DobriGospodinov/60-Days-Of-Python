import cv2
import streamlit as st
from datetime import datetime


st.title("Motion Detector")
start = st.button("Start Camera")


if start:
    streamlit_image = st.image([])
    camera = cv2.VideoCapture(0)

    while True:
        check, frame = camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Get current day and date
        now = datetime.now()
        day_of_week = now.strftime("%A")  # Full day name (e.g., "Monday")
        date_str = now.strftime("%Y-%m-%d")  # Date in "YYYY-MM-DD" format

        cv2.putText(img=frame,text=day_of_week, org=(10, 20),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(20, 100, 200), thickness=2, lineType=cv2.LINE_AA)

        cv2.putText(img=frame,text=date_str, org=(10, 40),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1,
                    color=(20, 100, 200), thickness=2, lineType=cv2.LINE_AA)

        streamlit_image.image(frame)