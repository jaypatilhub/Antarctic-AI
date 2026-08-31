
import streamlit as st
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

from data_module import load_data, validate_data, clean_data, preprocess_data
from risk_module import calculate_risk_from_data, get_risk_reason
from map_module import create_antarctic_map
from route_module import (
    recommend_route,
    calculate_fuel,
    compare_safety_fuel,
    rank_routes,
    replan_route,
    recommend_best_route
)


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
# NAVIGATION POINTS
# =========================================================

st.subheader("🚢 Navigation Points")

locations = {
    "McMurdo Station": (-77.8481, 166.6681),
    "Palmer Station": (-64.7798, -64.0553),
    "Rothera Research Station": (-67.5689, -68.1248),
    "Amundsen-Scott South Pole Station": (-90.0000, 0.0000),
    "Casey Station": (-66.2817, 110.5275),
    "Davis Station": (-68.5767, 77.9672),
    "Mawson Station": (-67.6028, 62.8744),
    "Halley Research Station": (-75.5682, -25.5085)
}

col1, col2 = st.columns(2)

with col1:
    start_location = st.selectbox(
        "Starting Point",
        list(locations.keys()),
        key="top_start_location"
    )

with col2:
    end_location = st.selectbox(
        "Destination",
        list(locations.keys()),
        index=1,
        key="top_end_location"
    )

start_lat, start_lon = locations[start_location]
end_lat, end_lon = locations[end_location]

st.info(
    f"Starting Point: {start_location} | "
    f"Destination: {end_location}"
)

ship_lat = start_lat
ship_lon = start_lon


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
    st.metric(
        "Icebergs Detected",
        len(df)
    )

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
# FUEL PARAMETERS
# =========================================================

st.subheader("⛽ Fuel Parameters")

col1, col2 = st.columns(2)

with col1:
    fuel_per_km = st.number_input(
        "Fuel Consumption (L/km)",
        min_value=0.1,
        value=2.0,
        step=0.1
    )

with col2:
    fuel_cost_per_liter = st.number_input(
        "Fuel Cost (per Liter)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )


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
# ROUTE RISK MAPPING
# =========================================================

if risk == "CRITICAL":
    route_ice_risk = "HIGH"
elif risk == "HIGH":
    route_ice_risk = "HIGH"
elif risk == "MEDIUM":
    route_ice_risk = "MEDIUM"
else:
    route_ice_risk = "LOW"


# =========================================================
# AI ROUTE RECOMMENDATION
# =========================================================

route_result = recommend_route(
    nearest_distance,
    route_ice_risk
)

st.subheader("🧭 AI Route Recommendation")

st.write(
    f"**Status:** {route_result['status']}"
)

st.write(
    f"**Recommendation:** {route_result['recommendation']}"
)

if "reason" in route_result:
    st.write(
        f"**Reason:** {route_result['reason']}"
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
    f"**Recommendation:** "
    f"{selected_route_result['recommendation']}"
)

if "reason" in selected_route_result:
    st.write(
        f"**Reason:** {selected_route_result['reason']}"
    )


# =========================================================
# FUEL ESTIMATION
# =========================================================

fuel_result = calculate_fuel(
    selected_distance,
    fuel_per_km,
    fuel_cost_per_liter
)

st.subheader("⛽ Selected Route Fuel Estimate")

st.write(
    f"**Estimated Fuel:** "
    f"{fuel_result['estimated_fuel_liters']:.2f} L"
)

st.write(
    f"**Estimated Fuel Cost:** "
    f"{fuel_result['estimated_fuel_cost']:.2f}"
)


# =========================================================
# SAFETY VS FUEL COMPARISON
# =========================================================

route_a = {
    "distance_km": route_a_distance,
    "ice_risk": route_ice_risk
}

route_b = {
    "distance_km": route_b_distance,
    "ice_risk": route_ice_risk
}

comparison = compare_safety_fuel(
    route_a,
    route_b,
    fuel_per_km,
    fuel_cost_per_liter
)

st.subheader("⚖️ Safety vs Fuel Comparison")

st.write(
    f"**Route A:** {comparison['route_a_risk']} | "
    f"{comparison['route_a_fuel_liters']:.2f} L"
)

st.write(
    f"**Route B:** {comparison['route_b_risk']} | "
    f"{comparison['route_b_fuel_liters']:.2f} L"
)

st.success(
    f"Recommended: {comparison['recommended_route']}"
)


# =========================================================
# ROUTE RANKING
# =========================================================

candidate_routes = [
    {
        "name": "Route A",
        "distance_km": route_a_distance,
        "ice_risk": route_ice_risk
    },
    {
        "name": "Route B",
        "distance_km": route_b_distance,
        "ice_risk": route_ice_risk
    },
    {
        "name": "Route C",
        "distance_km": route_c_distance,
        "ice_risk": route_ice_risk
    }
]

ranked_routes = rank_routes(
    candidate_routes,
    fuel_per_km,
    fuel_cost_per_liter
)

st.subheader("🏆 Route Ranking")

for route in ranked_routes:
    st.write(
        f"**{route['name']}** | "
        f"Risk: {route['risk']} | "
        f"Fuel: {route['fuel_liters']:.2f} L | "
        f"Cost: {route['fuel_cost']:.2f}"
    )


# =========================================================
# BEST ROUTE RECOMMENDATION
# =========================================================

best_route_result = recommend_best_route(
    candidate_routes
)

st.subheader("🧭 Best Route Recommendation")

st.write(
    f"**Status:** {best_route_result['status']}"
)

st.write(
    f"**Recommendation:** "
    f"{best_route_result['recommendation']}"
)

if best_route_result.get("route"):
    st.success(
        f"Selected Best Route: "
        f"{best_route_result['route']['name']} | "
        f"{best_route_result['route']['distance_km']:.2f} km"
    )


# =========================================================
# DYNAMIC RE-ROUTING
# =========================================================

current_route = {
    "name": selected_route,
    "distance_km": selected_distance,
    "ice_risk": route_ice_risk
}

alternative_routes = [
    route
    for route in candidate_routes
    if route["name"] != selected_route
]

replan_result = replan_route(
    current_route,
    alternative_routes
)

st.subheader("🔄 Dynamic Re-Routing")

st.write(
    f"**Status:** {replan_result['status']}"
)

st.write(
    f"**Recommendation:** "
    f"{replan_result['recommendation']}"
)

if replan_result.get("route"):
    st.success(
        f"Alternative Route: "
        f"{replan_result['route']['name']} | "
        f"{replan_result['route']['distance_km']:.2f} km"
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
