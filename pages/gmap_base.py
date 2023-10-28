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


st.set_page_config(layout="wide")

st.title("NeyJourNeyJour")

col1, col2 = st.columns([4, 1])

Map = geemap.Map()
Map.add_basemap("ESA WorldCover 2020 S2 FCC")
Map.add_basemap("ESA WorldCover 2020 S2 TCC")
Map.add_basemap("HYBRID")


sent2 = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").first()
sent2_vis = {"bands": ["B2","B3","B4"]}

esa = ee.ImageCollection("ESA/WorldCover/v100").first()
esa_vis = {"bands": ["Map"]}
#esri = ee.ImageCollection(
#    "projects/sat-io/open-datasets/landcover/ESRI_Global-LULC_10m"
#).mosaic()
#esri_vis = {
#    "min": 1,
#    "max": 10,
#    "palette": [
#        "#1A5BAB",
#        "#358221",
#        "#A7D282",
#        "#87D19E",
#        "#FFDB5C",
#        "#EECFA8",
#        "#ED022A",
#        "#EDE9E4",
#        "#F2FAFF",
#        "#C8C8C8",
#    ],
#}

dataset = (
    ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterDate('2018-01-01', '2022-01-30')
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
    .map(mask_s2_clouds)
)

visualization = {
    'min': 0.0,
    'max': 0.3,
    'bands': ['B4'],
}

#m = geemap.Map()
#m.set_center(83.277, 17.7009, 12)
#m.add_layer(dataset.mean(), visualization, 'RGB')
#   m

    
with col2:

    longitude = st.number_input("Longitude", -180.0, 180.0, 8.559718)
    latitude = st.number_input("Latitude", -90.0, 90.0, 49.794677)
    zoom = st.number_input("Zoom", 0, 20, 11)

    Map.setCenter(longitude, latitude, zoom)

    start = st.date_input("Start Date for Dynamic World", datetime.date(2020, 1, 1))
    end = st.date_input("End Date for Dynamic World", datetime.date(2021, 1, 1))

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    region = ee.Geometry.BBox(-179, -89, 179, 89)
    dw = geemap.dynamic_world(region, start_date, end_date, return_type="hillshade")

    layers = {
        "Dynamic World": (dw, {}, "Dynamic World Land Cover"),
        "ESA Land Cover": (esa, esa_vis, "ESA Land Cover"),
        "Sentinel 2 B4": (dataset, visualization, "Sentinel 2"),
        "Sentinel 2 [B2 - B8]": (sent2, sent2_vis, "Sentinel 2")
        #"ESRI Land Cover": (esri, esri_vis, "ESRI Land Cover"),
    }

    options = list(layers.keys())
    selected_layer_key = st.selectbox("Select a layer", options, index=0)
    
    Map.add_layer(*layers[selected_layer_key])
    
    #Map.addLayer(OverlayMap)
    #Map.split_map(left_layer, right_layer)

    #legend = st.selectbox("Select a legend", options, index=options.index(right))
    #if legend == "Dynamic World":
        #Map.add_legend(
            #title="Dynamic World Land Cover",
            #builtin_legend="Dynamic_World",
        #)
    #elif legend == "ESA Land Cover":
        #Map.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")
    #elif legend == "ESRI Land Cover":
        #Map.add_legend(title="ESRI Land Cover", builtin_legend="ESRI_LandCover")

with col1:
    Map.to_streamlit(height=750)