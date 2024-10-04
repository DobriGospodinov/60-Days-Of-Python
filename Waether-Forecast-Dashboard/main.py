import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, selectbox and subheader
st.title("Waether Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5, help="Select the number of forecasted days")
option = st.selectbox("Select data to view", ("Temperature", "Sky"))
st.subheader(f"{option} for the next {days} days in {place}")


if place:
    # Get the temperature/sky data
    filtered_data = get_data(place, days)

    if option == "Temperature":
        temperatures = [dict["main"]["temp"] for dict in filtered_data]
        temperatures = [float(temp / 10) for temp in temperatures]
        dates =[dict["dt_txt"] for dict in filtered_data]

        # Create temperature plot
        figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
        st.plotly_chart(figure)

# My solution to obtain the list of filepaths
    # if option == "Sky":
    #     sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
    #     image_filepaths = [f"images/{condition.lower()}.png" for condition in sky_conditions]
    #     st.image(image_filepaths, width=110)

# Alternative way to translate the conditions to image paths (which was the original course solution)
# a.k.a "data translation"

    if option == "Sky":
        sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
        dates = [dict["dt_txt"] for dict in filtered_data]
        images = {"Clear":"images/clear.png", "Clouds":"images/clouds.png", \
                  "Rain":"images/rain.png", "Snow":"images/snow.png"}
        image_filepaths = [images[condition] for condition in sky_conditions]
        st.image(image_filepaths, width=110, caption=dates)