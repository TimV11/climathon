import datetime
import ee
import streamlit as st
import geemap.foliumap as geemap

def mask_s2_clouds(image):
  """Masks clouds in a Sentinel-2 image using the QA band.

  Args:
      image (ee.Image): A Sentinel-2 image.

  Returns:
      ee.Image: A cloud-masked Sentinel-2 image.
  """
  qa = image.select('QA60')

  # Bits 10 and 11 are clouds and cirrus, respectively.
  cloud_bit_mask = 1 << 10
  cirrus_bit_mask = 1 << 11

  # Both flags should be set to zero, indicating clear conditions.
  mask = (
      qa.bitwiseAnd(cloud_bit_mask)
      .eq(0)
      .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
  )

  return image.updateMask(mask).divide(10000)

def set_time(image):
  return image.set({'system:time_start':image.date().millis()})

st.set_page_config(layout="wide")

st.title("CanopyAI")

col1, col2 = st.columns([4, 1])

Map = geemap.Map()

aoi = ee.Geometry.Polygon(
  [[[8.559718,  49.952662],
    [8.559718, 49.794677],
    [8.752842, 49.794677],
    [8.752842, 49.952662]]]
  )



sent2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").first()
sent2_vis = {"bands": ["B2","B3","B4"]}

esa = ee.ImageCollection("ESA/WorldCover/v100").first()
esa_vis = {"bands": ["Map"]}

vis_params = {
    'min': 0,
    'max': 3000,
    'bands': ['B4', 'B3', 'B2'],
    }

vis_ndvi_params = {
        'min': -1,
        'max': 0.5,
        'palette': ['0c8204','a3a3a3']
        }

vis_ndvi_delta = {
        'min': -0.05,
        'max': 0.05,
        'palette': ['FF5733', 'AAFF00']
        }

    
with col2:

    longitude = st.number_input("Longitude", -180.0, 180.0, 8.559718)
    latitude = st.number_input("Latitude", -90.0, 90.0, 49.794677)
    zoom = st.number_input("Zoom", 0, 20, 11)

    Map.setCenter(longitude, latitude, zoom)

    date = st.date_input("Date", datetime.date(2020, 1, 1))
    date_date = date.strftime("%Y-%m-%d")

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")


    # Sentinel 2 Visual params
    sentinel_2 = (
        ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
        .map(set_time)
        .filterBounds(aoi)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1))
    )


    # NDVI 
    NIR = sentinel_2.select('B4').first()
    Red = sentinel_2.select('B3').first()

    ndvi = NIR.subtract(Red).divide(NIR.add(Red))


    # NDVI DELTA
    NIR_first = sentinel_2.select('B4').first()
    Red_first = sentinel_2.select('B3').first()
    ndvi_first = NIR_first.subtract(Red_first).divide(NIR_first.add(Red_first))

    sentinel_2_backwards = sentinel_2.sort('system:time_start', False)
    NIR_last = sentinel_2_backwards.select('B4').first()
    Red_last = sentinel_2_backwards.select('B3').first()
    ndvi_last = NIR_last.subtract(Red_last).divide(NIR_last.add(Red_last))

    ndvi_diff = ndvi_last.subtract(ndvi_first)


    # NDVI DELTA - town
    # ndvi_diff_minus_town =  


    region = ee.Geometry.BBox(-179, -89, 179, 89)
    dw = geemap.dynamic_world(region, start_date, end_date, return_type="hillshade")

    layers = {
        "Dynamic World": (dw, {}, "Dynamic World Land Cover"),
        "ESA Land Cover": (esa, esa_vis, "ESA Land Cover"),
        "Sentinel 2 Visual Params": (sentinel_2, vis_params,"Sentinel 2 Visual Params"),
        "Sentinel 2 NDVI": (ndvi, vis_ndvi_params, "Sentinel 2 NDVI"),
        "NDVI Delta": (ndvi_diff, vis_ndvi_delta, "NDVI Delta"),
    }

    options = list(layers.keys())
    selected_layer_key = st.selectbox("Select a layer", options, index=0)
    
    Map.add_layer(*layers[selected_layer_key])
    
    if selected_layer_key == "Dynamic World":
        Map.add_legend(
            title="Dynamic World Land Cover",
            builtin_legend="Dynamic_World",
        )
    elif selected_layer_key == "ESA Land Cover":
        Map.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
    #elif legend == "Sentinel 2 Visual Params":
    #    Map.add_legend(title="Sentinel 2 Visual Params", builtin_legend="Sentinel 2")

with col1:
    Map.to_streamlit(height=750)