import streamlit as st
import streamlit.components.v1 as components

from map_module import create_antarctic_map


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


# =========================================================
# ANTARCTIC MAP
# =========================================================

m = create_antarctic_map()

map_html = m.get_root().render()

components.html(
    map_html,
    height=600,
    scrolling=False
)