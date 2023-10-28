import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide")


st.title("NeyJourNeyJour")

col1, col2 = st.columns([4, 1])

Map = geemap.Map()

def set_time(image):
  return image.set({'system:time_start':image.date().millis()})

aoi = ee.Geometry.Polygon(
  [[[8.559718,  49.952662],
    [8.559718, 49.794677],
    [8.752842, 49.794677],
    [8.752842, 49.952662]]]
  )

sentinel_2 = (
    ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
      .map(set_time)
      .filterBounds(aoi)
      .filterDate('2017-04-01', '2023-10-27')
      .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1))
)

markdown = """
    - [Dynamic World Land Cover](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1?hl=en)
    - [ESA Global Land Cover](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100)
    - [ESRI Global Land Cover](https://samapriya.github.io/awesome-gee-community-datasets/projects/esrilc2020)

"""

with col2:

    longitude = st.number_input("Longitude", -180.0, 180.0, 8.6512)
    latitude = st.number_input("Latitude", -90.0, 90.0, 49.8728)
    zoom = st.number_input("Zoom", 0, 20, 11)

    Map.setCenter(longitude, latitude, zoom)

    date = st.date_input("Date", datetime.date(2020, 1, 1))
    date_date = date.strftime("%Y-%m-%d")

    vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2'],
    }

    vis_ndvi_params = {
        'min': -1,
        'max': 0.5,
        'palette': ['FFFFFF', 'AAFF00']
        }
    
    vis_ndvi_delta = {
        'min': -0.05,
        'max': 0.05,
        'palette': ['FF5733', 'AAFF00']
        }

    NIR_first = sentinel_2.select('B4').first()
    Red_first = sentinel_2.select('B3').first()
    ndvi_first = NIR_first.subtract(Red_first).divide(NIR_first.add(Red_first))

    sentinel_2_backwards = sentinel_2.sort('system:time_start', False)
    NIR_last = sentinel_2_backwards.select('B4').first()
    Red_last = sentinel_2_backwards.select('B3').first()
    ndvi_last = NIR_last.subtract(Red_last).divide(NIR_last.add(Red_last))

    ndvi_diff = ndvi_last.subtract(ndvi_first)

    Map.add_layer(sentinel_2, vis_params,"sentinel_2")
    Map.add_layer(ndvi_first,vis_ndvi_params,"NDVI first")
    Map.add_layer(ndvi_last,vis_ndvi_params,"NDVI last")
    Map.add_layer(ndvi_diff,vis_ndvi_delta,"NDVI diff")





with col1:
    Map.to_streamlit(height=750)