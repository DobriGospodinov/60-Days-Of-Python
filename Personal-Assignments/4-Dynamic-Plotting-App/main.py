import streamlit as st
import pandas as pd
import plotly.express as px

st.title("In Search for Happines")
option_x = st.selectbox("Select the data for the X-axis", ("GDP", "Happiness", "Generosity"))
option_y = st.selectbox("Select the data for the Y-axis", ("GDP", "Happiness", "Generosity"))
st.subheader(f"{option_x} and {option_y}")

df = pd.read_csv("happy.csv")

data_x = option_x.lower()
data_y = option_y.lower()

x = df[f"{data_x}"].tolist()
y = df[f"{data_y}"].tolist()

figure = px.scatter(x=x, y=y, labels={"x": f"{option_x}", "y": f"{option_y}"})
st.plotly_chart(figure)
