import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="Antarctic AI Navigation",
    page_icon="🧊"
)

st.title("🧊 Antarctic AI Navigation System")

st.write(
    "AI-based Antarctic Sea-Ice, "
    "Iceberg Trajectory and Navigation "
    "Decision Support System"
)

st.success("System Online")

m = folium.Map(location=[-75, 0], zoom_start=3)
folium.Marker([-75, 0], popup="Sample Iceberg").add_to(m)
st.write("Iceberg marker added")
folium.Marker(
    [-75, 0],
    popup="Antarctic Research Point"
).add_to(m)

folium.Circle(
    location=[-72, 20],
    radius=500000,
    popup="AI Risk Zone"
).add_to(m)

st_folium(m, width=900, height=600)