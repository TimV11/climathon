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
    #layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 10px;
    }
            
    
    .stTabs [data-baseweb="tab"] {
        flex: 1;
    }

	.stTabs [data-baseweb="tab"] {
		height: 50px;
        white-space: pre-wrap;
		background-color: #F0F2F6;
		border-radius: 4px 4px 4px 4px;
		gap: 10px;
		padding-top: 10px;
		padding-bottom: 10px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #FFFFFF;
	}

</style>""", unsafe_allow_html=True)

logo = Image.open('./pics/CanopyAI.png')
st.image(logo)

listTabs = ["  Our purpose  ", "  Case study: Darmstadt  ", "  About us  "]
tabs = st.tabs(listTabs)

with tabs[0]:
    
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

    st.subheader("📬 Get in Touch.")

    st.markdown('<a href="mailto:contact@climathon.digital">Contact us !</a>', unsafe_allow_html=True)

    #Footer:
    #Copyright Information: "© [Current Year] CanopyAI. All Rights Reserved."

with tabs[1]:
    with st.sidebar:
        if st.button('centralize '):
            pdk.View(
                longitude=8.65027, latitude=49.87167 , zoom=11, min_zoom=5, max_zoom=15, pitch=0, bearing=0
            )
            st.write('centralized to darmstadt')
        else:
            st.write('')
    st.link_button("Get started", "http://climathon.digital:8501/gmap_base")
    

with tabs[2]:
    col1, col2, col3 , col4, col5 = st.columns(5)


    # List of image file paths
    image_paths = [ 
        './pics/alfred.jpg', 
        './pics/theo.jpg',
        './pics/tim.jpg',
        './pics/niclas.jpg',
        './pics/benno.jpg']




    # List of image file paths and corresponding names
    image_data = [
        {"path": './pics/niclas.jpg', "name": "Niclas"},
        {"path": './pics/tim.jpg',    "name": "Tim"},
        {"path": './pics/theo.jpg',   "name": "Theo"},
        {"path": './pics/benno.jpg',  "name": "Benno"},
        {"path": './pics/alfred.jpg', "name": "Alfred"},
    ]

    # Create a row to display images and names horizontally
    row = st.columns(len(image_data))

    # Display images and names in the row
    for i, col in enumerate(row):
        col.image(image_data[i]["path"], caption=image_data[i]["name"], use_column_width=True)

