    
    
    
import datetime
import json
import ee
import streamlit as st
import geemap.foliumap as geemap



st.set_page_config(layout="wide")

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



st.title("Map Analytics")

col1, col2 = st.columns([4, 1])

Map = geemap.Map()
# Map.add_basemap("ESA WorldCover 2020 S2 FCC")
# Map.add_basemap("ESA WorldCover 2020 S2 TCC")
Map.add_basemap("HYBRID")

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

ndvi_forest = {
   'min': 0,
   'max': 0.1,
   'palette':['FFFFFF','FF0000'],
   'opacity':0.3,
}

    
with col2:

    longitude = st.number_input("Longitude", -180.0, 180.0, 8.559718)
    latitude = st.number_input("Latitude", -90.0, 90.0, 49.794677)
    zoom = st.number_input("Zoom", 0, 20, 11)

    Map.setCenter(longitude, latitude, zoom)

    start = st.date_input("Start Date for Dynamic World", datetime.date(2018, 8, 1))
    end = st.date_input("End Date for Dynamic World", datetime.date(2021, 8, 1))

    start_date = start.strftime("%Y-%m-%d")
    end_date = end.strftime("%Y-%m-%d")

    # load Forests
    list_polygons = json.load(open('forest_polygons/forest.json'))
    out_list = []
    for poly in list_polygons:
       out_list.append(ee.Geometry.Polygon(poly['coordinates']))
    forest_polygon = ee.Geometry.MultiPolygon(out_list)

    # Dynamic World Land Cover
    region = ee.Geometry.BBox(-179, -89, 179, 89)
    dw = geemap.dynamic_world(region, start_date, end_date, return_type="hillshade")

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
    # dw 
    # forest = ee.ImageCollection('JAXA/ALOS/PALSAR/YEARLY/FNF').filterDate('2017-01-01', '2017-12-31').first()
    
    ndvi_diff_only_forest = ndvi_diff.clip(forest_polygon)

    #mask = ee.Image(dw).eq(1)
    #ndvi_diff_minus_town = dw.filter(ee.Filter.eq(1)).geometry()



    layers = {
        "NDVI Delta only Forest": (ndvi_diff_only_forest, ndvi_forest, "NDVI Delta only Forest"),
        "default":(0,0,0),
        "Dynamic World": (dw, {}, "Dynamic World Land Cover"),
        "ESA Land Cover": (esa, esa_vis, "ESA Land Cover"),

        "Sentinel 2 Visual Params": (sentinel_2, vis_params,"Sentinel 2 Visual Params"),
        "Sentinel 2 NDVI": (ndvi, vis_ndvi_params, "Sentinel 2 NDVI"),
        "NDVI Delta": (ndvi_diff, vis_ndvi_delta, "NDVI Delta"),
    }

    options = list(layers.keys())
    selected_layer_key = st.selectbox("Select a layer", options, index=0)
    if not selected_layer_key == "default":
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