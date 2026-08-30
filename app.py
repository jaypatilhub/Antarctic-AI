import streamlit as st
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

from data_module import load_data, validate_data, clean_data, preprocess_data
from risk_module import calculate_risk_from_data, get_risk_reason
from map_module import create_antarctic_map
from route_module import recommend_route


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Antarctic AI Navigation",
    page_icon="🧊",
    layout="wide"
)


# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two latitude/longitude points."""

    earth_radius_km = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


# =========================================================
# HEADER
# =========================================================

st.title("🧊 Antarctic AI Navigation System")

st.write(
    "AI-based Antarctic Sea-Ice, Iceberg Trajectory and "
    "Navigation Decision Support System"
)

st.success("🟢 System Online")


# =========================================================
# LOAD AND PROCESS DATA
# =========================================================

try:
    df = load_data()

    validate_data(df)

    df = clean_data(df)

    df = preprocess_data(df)

except Exception as e:
    st.error(f"Data processing error: {e}")
    st.stop()


# =========================================================
# DATA SUMMARY
# =========================================================

st.subheader("📊 Antarctic Data")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Icebergs Detected", len(df))

with col2:
    st.metric(
        "Average Sea-Ice",
        f"{df['sea_ice_concentration'].mean():.1f}%"
    )

with col3:
    st.metric(
        "Maximum Sea-Ice",
        f"{df['sea_ice_concentration'].max():.1f}%"
    )

st.dataframe(
    df,
    use_container_width=True
)


# =========================================================
# VESSEL POSITION
# =========================================================

st.subheader("🚢 Navigation Points")

col1, col2 = st.columns(2)

with col1:
    start_lat = st.number_input(
        "Start Latitude",
        value=-70.0,
        min_value=-90.0,
        max_value=90.0
    )

    start_lon = st.number_input(
        "Start Longitude",
        value=20.0,
        min_value=-180.0,
        max_value=180.0
    )

with col2:
    end_lat = st.number_input(
        "End Latitude",
        value=-68.0,
        min_value=-90.0,
        max_value=90.0
    )

    end_lon = st.number_input(
        "End Longitude",
        value=30.0,
        min_value=-180.0,
        max_value=180.0
    )

ship_lat = start_lat
ship_lon = start_lon
# =========================================================
# ROUTE DISTANCE
# =========================================================

route_distance = calculate_distance_km(
    start_lat,
    start_lon,
    end_lat,
    end_lon
)

st.metric(
    "Start → End Distance",
    f"{route_distance:.2f} km"
)
# =========================================================
# CANDIDATE ROUTES
# =========================================================

route_a_distance = route_distance
route_b_distance = route_distance * 1.08
route_c_distance = route_distance * 1.15

routes = {
    "Route A": route_a_distance,
    "Route B": route_b_distance,
    "Route C": route_c_distance
}

st.subheader("🛳️ Candidate Routes")

for route_name, distance in routes.items():
    st.write(
        f"**{route_name}:** {distance:.2f} km"
    )
    # =========================================================
# ROUTE SELECTION
# =========================================================

selected_route = st.selectbox(
    "Select Route",
    list(routes.keys())
)

selected_distance = routes[selected_route]

st.info(
    f"Selected Route: {selected_route} | "
    f"Distance: {selected_distance:.2f} km"
)


# =========================================================
# AUTOMATIC NEAREST ICEBERG ANALYSIS
# =========================================================

distances = []

for _, row in df.iterrows():

    distance_km = calculate_distance_km(
        ship_lat,
        ship_lon,
        row["latitude"],
        row["longitude"]
    )

    distances.append(distance_km)

df["distance_from_vessel_km"] = distances

nearest_index = df["distance_from_vessel_km"].idxmin()

nearest_iceberg = df.loc[nearest_index]

nearest_iceberg_id = nearest_iceberg["iceberg_id"]
nearest_distance = nearest_iceberg["distance_from_vessel_km"]
nearest_sea_ice = nearest_iceberg["sea_ice_concentration"]


# =========================================================
# RISK ANALYSIS
# =========================================================

st.subheader("⚠️ AI Risk Analysis")

risk = calculate_risk_from_data(
    nearest_distance,
    nearest_sea_ice
)

reason = get_risk_reason(nearest_distance)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Nearest Iceberg",
        nearest_iceberg_id
    )

with col2:
    st.metric(
        "Distance",
        f"{nearest_distance:.2f} km"
    )

with col3:
    st.metric(
        "Sea-Ice",
        f"{nearest_sea_ice:.1f}%"
    )

st.metric(
    "Overall Risk",
    risk
)

st.info(
    f"Risk Reason: {reason}"
)


# =========================================================
# ROUTE RECOMMENDATION
# =========================================================

st.subheader("🧭 AI Route Recommendation")

if risk == "CRITICAL":
    route_ice_risk = "HIGH"
elif risk == "HIGH":
    route_ice_risk = "HIGH"
elif risk == "MEDIUM":
    route_ice_risk = "MEDIUM"
else:
    route_ice_risk = "LOW"


route_result = recommend_route(
    nearest_distance,
    route_ice_risk
)
# =========================================================
# SELECTED ROUTE RISK
# =========================================================

selected_route_result = recommend_route(
    selected_distance,
    route_ice_risk
)

st.subheader("⚠️ Selected Route Risk")

st.write(
    f"**Selected Route:** {selected_route}"
)

st.write(
    f"**Safety Status:** {selected_route_result['status']}"
)

st.write(
    f"**Recommendation:** {selected_route_result['recommendation']}"
)

st.write(
    f"**Route Status:** {route_result['status']}"
)

st.write(
    f"**Recommendation:** {route_result['recommendation']}"
)

if "reason" in route_result:
    st.write(
        f"**Reason:** {route_result['reason']}"
    )


# =========================================================
# ANTARCTIC MAP
# =========================================================

st.subheader("🌍 Antarctic AI Monitoring Map")

try:
    antarctic_map = create_antarctic_map()

    st_folium(
        antarctic_map,
        width=1200,
        height=650
    )

except Exception as e:
    st.error(
        f"Map loading error: {e}"
    )


# =========================================================
# SYSTEM STATUS
# =========================================================

st.subheader("🟢 System Status")

st.write("✅ M2 — Antarctic Map Module")
st.write("✅ M3 — Data Processing Module")
st.write("✅ M4 — Risk Analysis Module")
st.write("✅ M5 — Route Recommendation Module")
st.write("🚀 M1 — Main Application Integration") 