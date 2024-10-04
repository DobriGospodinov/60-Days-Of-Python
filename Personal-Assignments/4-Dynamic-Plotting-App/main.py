import streamlit as st
import pandas as pd
import plotly.express as px

st.title("In Search for Happines")
option1 = st.selectbox("Select the data for the X-axis", ("GDP", "Happiness", "Generosity"))
option2 = st.selectbox("Select the data for the Y-axis", ("GDP", "Happiness", "Generosity"))
st.subheader(f"{option1} and {option2}")

df = pd.read_csv("happy.csv")

data1 = option1.lower()
data2 = option2.lower()

x = df[f"{data1}"].tolist()
y = df[f"{data2}"].tolist()

figure = px.scatter(x=x, y=y, labels={"x": f"{option1}", "y": f"{option2}"})
st.plotly_chart(figure)
