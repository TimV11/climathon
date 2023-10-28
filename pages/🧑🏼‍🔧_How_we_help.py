import streamlit as st


st.set_page_config(
    layout="centered",
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


# Title
st.title("Enhancing Forest Health with Satellite Technology")

# Introduction
st.write("Forests are vital ecosystems that provide a wide range of benefits, from clean air and water to biodiversity conservation. For foresters, ensuring the health and sustainability of these natural habitats is of paramount importance. In today's digital age, technology, including satellite technology, plays a significant role in this endeavor. Here, we explore how foresters can leverage satellite data to protect and improve forest health.")

# Sections
st.header("1. Monitoring Forest Health")
st.write("Satellite imagery allows foresters to monitor the state of the forest from above. With the help of specialized satellite sensors, they can detect changes in forest cover, identify stressed or unhealthy areas, and assess the impact of factors like climate change, disease outbreaks, and deforestation.")

st.header("2. Early Detection of Threats")
st.write("Satellites provide an invaluable tool for early threat detection. They can track the spread of pests and diseases, such as bark beetles or invasive species, allowing foresters to respond promptly and contain the threat before it becomes a full-blown crisis.")

st.header("3. Fire Management")
st.write("Fire management is a critical aspect of forest health. Satellites can aid in fire prevention and management by providing real-time information on fire hotspots, fire progression, and smoke dispersion. This data is essential for planning controlled burns and protecting the forest from catastrophic wildfires.")

st.header("4. Sustainable Harvesting")
st.write("Foresters can use satellite technology to plan and monitor sustainable timber harvesting. By analyzing forest data from satellites, they can ensure that logging activities are within sustainable limits, reducing the risk of overharvesting and forest degradation.")

st.header("5. Biodiversity Conservation")
st.write("Satellites also play a role in biodiversity conservation. By tracking changes in land cover and identifying potential habitat disruptions, foresters can take action to protect and restore habitats for various plant and animal species within the forest.")

st.header("6. Research and Long-Term Planning")
st.write("With long-term satellite data, foresters can conduct research to understand how forests evolve over time. This knowledge is essential for long-term planning, ensuring that the forest remains healthy for generations to come.")
