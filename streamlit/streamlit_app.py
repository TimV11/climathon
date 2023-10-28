import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import pydeck as pdk
import xarray
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

st.write("# CanopyAI 🌳👑")

tab1, tab2, tab3 = st.tabs(["landing page", "interactive map", "about us"])

with tab1:
    # Using object notation
    # Erstelle einen Date/Time-Schieberegler mit einem Wochenbereich
    start_date = datetime(2020, 1, 1)
    end_date = start_date + timedelta(weeks=100)

    selected_date = st.sidebar.slider(
        "Select a date range",
        min_value=start_date,
        max_value=end_date,
        value=(start_date, end_date),
        step=timedelta(days=1),
    )
    num_turns = st.sidebar.slider("some bullshit", 1, 100, 9)

    add_selectbox = st.sidebar.selectbox(
        "Background map",
        ("default", "terrain", "satellite")
    )

    # Using "with" notation
    with st.sidebar:
        add_radio = st.radio(
            "Choose a indicator",
            ("dry", "wet", "ligma")
        )

    with st.sidebar:
        st.button("Reset", type="primary")
        if st.button('centralize '):
            pdk.View(
                longitude=8.65027, latitude=49.87167 , zoom=11, min_zoom=5, max_zoom=15, pitch=0, bearing=0
            )
            st.write('centralized to darmstadt')
        else:
            st.write('fuck off')

with tab2:
    # Load xarray dataset 
    ds = xarray.open_dataset("load-raw.nc")

    data_array = ds["B04"]

    # Define the coordinates bounding box
    bounding_box = {
        "west": 8.559718,
        "south": 49.794677,
        "east": 8.752842,
        "north": 49.952662,
    }

    # Generate latitude and longitude coordinates within the bounding box
    latitudes = np.linspace(bounding_box['south'], bounding_box['north'], data_array.shape[-2])
    longitudes = np.linspace(bounding_box['west'], bounding_box['east'], data_array.shape[-1])

    # Create coordinates for the heatmap
    grid = np.meshgrid(longitudes, latitudes)
    coordinates = np.stack((grid[0], grid[1]), axis=-1).reshape(-1, 2)


    # PyDeck View State focused on bounding box
    view_state = pdk.ViewState(
        latitude=(bounding_box['south'] + bounding_box['north']) / 2,
        longitude=(bounding_box['west'] + bounding_box['east']) / 2,
        zoom=10
    )

    weights = data_array.isel(t=0)
    df = data_array.isel(t=0).to_dataframe()

    # PyDeck Scatterplot Layer
    scatterplot_layer = pdk.Layer(
        "ScatterplotLayer",
        data=coordinates,
        get_position="[0, 1]",
        get_radius=50,  # Change the radius value as needed
        get_fill_color="[255, weights, 255]",  # Adjust color attributes using weights
        pickable=True,
        opacity=0.8
    )

    scatterplot_layer2 = pdk.Layer(
        "Scatterplotlayer",
        df,
        get_position="[0,1]",
        
    )

    pydeck_chart = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state=view_state,
        # layers= [scatterplot_layer]
    )

    st.pydeck_chart(pydeck_chart)

with tab3:

    # col1, col2, col3 , col4, col5= st.columns(5, gap="large")

    st.header("Theo")
    theo = Image.open('./pics/theo.jpg').resize((400, 400))
    st.image(theo, caption='https://www.linkedin.com/in/theodor-nguyen-816269133/')

    st.header("Tim")
    tim = Image.open('./pics/tim.jpg').resize((400, 400))
    st.image(tim, caption='https://www.linkedin.com/in/tim%2Dvielhauer%2D66984026b/')

    st.header("Alfred")
    alfred = Image.open('./pics/alfred.jpg').resize((400, 400))
    st.image(alfred, caption='https://www.linkedin.com/in/alfred-quan-anh-nguyen/')

    st.header("Niclas")
    niclas = Image.open('./pics/niclas.jpg').resize((400, 400))
    st.image(niclas, caption='https://www.linkedin.com/in/niclas-schilling/')

    st.header("Benno")
    benno = Image.open('./pics/benno.jpg').resize((400, 400))
    st.image(benno, caption='https://www.linkedin.com/in/benno-koesters/')
    
