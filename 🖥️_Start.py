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
    #initial_sidebar_state="collapsed",
)

st.sidebar.title("Contact Us")
st.sidebar.info(
    """ [Send us an E-Mail!](mailto:contact@climathon.digital) """
)

st.sidebar.title("Source Code")
st.sidebar.info(

    """
    - Web App URL: <http://climathon.digital:8501/>
    - Our GitHub Repository: <https://github.com/TimV11/climathon>
    """
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

st.header("Revitalizing Forests with Satellite Intelligence")
with st.container():
    st.subheader("CanopyAI: Your Forest's Guardian")
with st.container():
    st.subheader("Who We Are")
st.write("At CanopyAI, we're on a mission to use cutting-edge technology for sustainable forest preservation. Through advanced data analysis, powered by the Sentinel 2 mission, we're committed to safeguarding and revitalizing our forests, ensuring a greener, more sustainable future for all.")
st.subheader("What We Do.")
st.markdown("**Satellite Data Analysis**")
st.write("We harness data from the Sentinel 2 mission to monitor the health of your forest, capturing every detail from above.")
st.markdown("**Machine Learning Insights**")
st.write("Our advanced machine learning algorithms analyze this data to predict forest conditions and assess environmental impact.")
st.markdown("**Actionable Recommendations**")
st.write("We deliver actionable recommendations, empowering you to take effective measures for forest revitalization.")

st.subheader("📬 Get in Touch")

image_data = [
    {"path": './pics/niclas.jpg',"text": "Lorem ipsum" , "name": "Niclas" , "link" :'https://www.linkedin.com/in/niclas-schilling/'          },
    {"path": './pics/tim.jpg',   "text": "Lorem ipsum" , "name": "Tim"    , "link" :'https://www.linkedin.com/in/tim%2Dvielhauer%2D66984026b/'  },
    {"path": './pics/theo.jpg',  "text": "Lorem ipsum" , "name": "Theo"   , "link" :'https://www.linkedin.com/in/theodor-nguyen-816269133/'     },
    {"path": './pics/benno.jpg', "text": "Lorem ipsum" , "name": "Benno"  , "link" :'https://www.linkedin.com/in/benno-koesters/'             },
    {"path": './pics/alfred.jpg',"text": "Lorem ipsum" , "name": "Alfred" , "link" :'https://www.linkedin.com/in/alfred-quan-anh-nguyen/'    }
]







# Create a row to display images and names horizontally
row = st.columns(len(image_data))

# Display images and names in the row
for i, col in enumerate(row):
    col.image(image_data[i]["path"], 
              caption= image_data[i]["name"],
              #caption= "[" + image_data[i]["name"] + "]" + "(" + image_data[i]["link"] + ")",
              use_column_width=True)















