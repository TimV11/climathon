import pandas as pd
import streamlit as st
import numpy as np
from PIL import Image
import pydeck as pdk
import xarray
import matplotlib.pyplot as plt

from datetime import datetime, timedelta

# ------------------------------------------------------------
#
#                  Visual settings
#
# ------------------------------------------------------------

st.set_page_config(
     initial_sidebar_state="collapsed",
)






logo = Image.open('./pics/CanopyAI.png')
st.image(logo)

tab1, tab2, tab3 = st.tabs(["Our purpose", "Case study: Darmstadt", "About us"])

with tab1:
    
    st.header("Revitalizing Forests with Satellite Intelligence.")
    with st.container():
        st.subheader("CanopyAI: Your Forest's Guardian.")
        st.link_button("Get started", "http://climathon.digital:8501/gmap_base")


    with st.container():
        st.subheader("Who We Are.")
    st.write("At CanopyAI, we're on a mission to use cutting-edge technology for sustainable forest preservation. Through advanced data analysis, powered by the Sentinel 2 mission, we're committed to safeguarding and revitalizing our forests, ensuring a greener, more sustainable future for all.")

    st.subheader("What We Do.")
    st.markdown("**Satellite Data Analysis**")
    st.write("We harness data from the Sentinel 2 mission to monitor the health of your forest, capturing every detail from above.")
    st.markdown("**Machine Learning Insights**")
    st.write("Our advanced machine learning algorithms analyze this data to predict forest conditions and assess environmental impact.")
    st.markdown("**Actionable Recommendations**")
    st.write("We deliver actionable recommendations, empowering you to take effective measures for forest revitalization.")

    st.subheader("Get in Touch.")

    st.markdown('<a href="mailto:contact@climathon.digital">Contact us !</a>', unsafe_allow_html=True)

    #Footer:
    #Copyright Information: "© [Current Year] CanopyAI. All Rights Reserved."

with tab2:
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


    "TODO insert smth here"

with tab3:

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.header("Theo")
        theo = Image.open('./pics/theo.jpg').resize((400, 400))
        st.image(theo, caption='https://www.linkedin.com/in/theodor-nguyen-816269133/')

    with col2:
        st.header("Tim")
        tim = Image.open('./pics/tim.jpg').resize((400, 400))
        st.image(tim, caption='https://www.linkedin.com/in/tim%2Dvielhauer%2D66984026b/')

    with col3:
        st.header("Alfred")
        alfred = Image.open('./pics/alfred.jpg').resize((400, 400))
        st.image(alfred, caption='https://www.linkedin.com/in/alfred-quan-anh-nguyen/')

    col4, col5 = st.columns(2, gap="large")
    with col4:
        st.header("Niclas")
        niclas = Image.open('./pics/niclas.jpg').resize((400, 400))
        st.image(niclas, caption='https://www.linkedin.com/in/niclas-schilling/')

    with col5:
        st.header("Benno")
        benno = Image.open('./pics/benno.jpg').resize((400, 400))
        st.image(benno, caption='https://www.linkedin.com/in/benno-koesters/')
    
