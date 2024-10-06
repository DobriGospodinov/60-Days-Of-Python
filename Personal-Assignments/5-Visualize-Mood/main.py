import streamlit as st
import plotly.express as px
import glob
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime


# Parse data
filepaths = sorted(glob.glob("diary/*.txt"))
analyzer = SentimentIntensityAnalyzer()
positivity = []
negativity = []
dates = []


for filepath in filepaths:
    with open(filepath, 'r') as file:
        content = file.readline()
    sentiment = analyzer.polarity_scores(content)
    positivity.append(sentiment["pos"])
    negativity.append(sentiment["neg"])
    date = filepath[6:16]
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y-%b-%d")
    dates.append(formatted_date)

# Genetare website
st.title("Diary Tone")

st.subheader("Positivity")
figure = px.line(x=dates, y=positivity, labels={"x": "Date", "y": "Positivity"})
st.plotly_chart(figure)

st.subheader("Negativity")
figure = px.line(x=dates, y=negativity, labels={"x": "Date", "y": "Negativity"})
st.plotly_chart(figure)
