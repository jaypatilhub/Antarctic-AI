
import streamlit as st
from streamlit_folium import st_folium
from math import radians, sin, cos, sqrt, atan2

from data_module import (
    load_data,
    validate_data,
    clean_data,
    preprocess_data
)

from risk_module import (
    calculate_risk_from_data,
    get_risk_reason
)

from map_module import create_antarctic_map

from ai_prediction_module import get_ai_predictions

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
# MAP VIEW STATE
# =========================================================

if "map_expanded" not in st.session_state:
    st.session_state.map_expanded = False

# Map fullscreen mode
if "map_fullscreen" not in st.session_state:
    st.session_state.map_fullscreen = False

# =========================================================
# DISTANCE CALCULATION
# =========================================================

def calculate_distance_km(lat1, lon1, lat2, lon2):

    earth_radius_km = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

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

    st.error(
        f"Data processing error: {e}"
    )

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
    width="stretch"
)


# =========================================================
# AI PREDICTION
# =========================================================

st.subheader("🤖 AI Prediction")

try:

    ai_predictions = get_ai_predictions(
        days_ahead=3
    )

    st.success(
        f"Prediction Status: "
        f"{ai_predictions['prediction_status']}"
    )

    st.subheader("🧊 Sea-Ice Forecast")

    sea_ice_predictions = ai_predictions[
        "sea_ice_prediction"
    ]

    st.dataframe(
        sea_ice_predictions,
        width="stretch"
    )

    st.subheader(
        "🧊 Iceberg Trajectory Forecast"
    )

    iceberg_predictions = ai_predictions[
        "iceberg_prediction"
    ]

    st.dataframe(
        iceberg_predictions,
        width="stretch"
    )

except Exception as e:

    st.error(
        f"AI prediction error: {e}"
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
        f"**{route_name}:** "
        f"{distance:.2f} km"
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
# NEAREST ICEBERG ANALYSIS
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

nearest_index = (
    df["distance_from_vessel_km"].idxmin()
)

nearest_iceberg = df.loc[
    nearest_index
]

nearest_iceberg_id = (
    nearest_iceberg["iceberg_id"]
)

nearest_distance = (
    nearest_iceberg["distance_from_vessel_km"]
)

nearest_sea_ice = (
    nearest_iceberg["sea_ice_concentration"]
)


# =========================================================
# RISK ANALYSIS
# =========================================================

st.subheader("⚠️ AI Risk Analysis")

risk = calculate_risk_from_data(
    nearest_distance,
    nearest_sea_ice
)

reason = get_risk_reason(
    nearest_distance
)

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

    route_ice_risk = "CRITICAL"

elif risk == "HIGH":

    route_ice_risk = "HIGH"

elif risk == "MEDIUM":

    route_ice_risk = "MEDIUM"

else:

    route_ice_risk = "LOW"


# =========================================================
# SELECTED ROUTE RISK
# =========================================================

st.subheader("🛡️ Selected Route Risk")

selected_route_result = recommend_route(
    selected_distance,
    route_ice_risk
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Route Risk",
        selected_route_result["status"]
    )

with col2:

    st.write(
        f"**Reason:** "
        f"{selected_route_result['reason']}"
    )

st.info(
    f"Recommendation: "
    f"{selected_route_result['recommendation']}"
)


# =========================================================
# FUEL ESTIMATION
# =========================================================

st.subheader("⛽ Fuel Estimate")

fuel_result = calculate_fuel(
    selected_distance,
    fuel_per_km,
    fuel_cost_per_liter
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Estimated Fuel",
        f"{fuel_result['estimated_fuel_liters']:.2f} L"
    )

with col2:

    st.metric(
        "Estimated Fuel Cost",
        f"₹{fuel_result['estimated_fuel_cost']:.2f}"
    )


# =========================================================
# BUILD ROUTE DATA
# =========================================================

route_a_fuel = calculate_fuel(
    route_a_distance,
    fuel_per_km,
    fuel_cost_per_liter
)

route_b_fuel = calculate_fuel(
    route_b_distance,
    fuel_per_km,
    fuel_cost_per_liter
)

route_c_fuel = calculate_fuel(
    route_c_distance,
    fuel_per_km,
    fuel_cost_per_liter
)


# =========================================================
# PROTOTYPE ROUTE-SPECIFIC RISK
# =========================================================

if route_ice_risk == "CRITICAL":

    route_a_risk = "CRITICAL"
    route_b_risk = "HIGH"
    route_c_risk = "MEDIUM"

elif route_ice_risk == "HIGH":

    route_a_risk = "HIGH"
    route_b_risk = "MEDIUM"
    route_c_risk = "LOW"

elif route_ice_risk == "MEDIUM":

    route_a_risk = "MEDIUM"
    route_b_risk = "LOW"
    route_c_risk = "LOW"

else:

    route_a_risk = "LOW"
    route_b_risk = "LOW"
    route_c_risk = "LOW"


route_data = [
    {
        "name": "Route A",
        "distance_km": route_a_distance,
        "risk_level": route_a_risk,
        "ice_risk": route_a_risk,
        "fuel_cost": route_a_fuel["estimated_fuel_cost"]
    },
    {
        "name": "Route B",
        "distance_km": route_b_distance,
        "risk_level": route_b_risk,
        "ice_risk": route_b_risk,
        "fuel_cost": route_b_fuel["estimated_fuel_cost"]
    },
    {
        "name": "Route C",
        "distance_km": route_c_distance,
        "risk_level": route_c_risk,
        "ice_risk": route_c_risk,
        "fuel_cost": route_c_fuel["estimated_fuel_cost"]
    }
]


# =========================================================
# SAFETY VS FUEL COMPARISON
# =========================================================

st.subheader("⚖️ Safety vs Fuel Comparison")

comparison = compare_safety_fuel(
    route_data[0],
    route_data[1],
    fuel_per_km,
    fuel_cost_per_liter
)

comparison_table = [
    {
        "Route": "Route A",
        "Risk": comparison["route_a_risk"],
        "Fuel (L)": comparison["route_a_fuel_liters"],
        "Fuel Cost": comparison["route_a_fuel_cost"]
    },
    {
        "Route": "Route B",
        "Risk": comparison["route_b_risk"],
        "Fuel (L)": comparison["route_b_fuel_liters"],
        "Fuel Cost": comparison["route_b_fuel_cost"]
    }
]

st.dataframe(
    comparison_table,
    width="stretch"
)

st.info(
    f"Safety vs Fuel Recommendation: "
    f"{comparison['recommended_route']}"
)


# =========================================================
# ROUTE RANKING
# =========================================================

st.subheader("🏆 Route Ranking")

ranked_routes = rank_routes(
    route_data,
    fuel_per_km,
    fuel_cost_per_liter
)

ranking_table = []

for index, route in enumerate(ranked_routes, start=1):

    ranking_table.append(
        {
            "Rank": index,
            "Route": route["name"],
            "Distance (km)": round(
                route["distance_km"],
                2
            ),
            "Risk": route["risk_level"],
            "Fuel Cost": round(
                route["fuel_cost"],
                2
            ),
            "Score": round(
                route["score"],
                2
            )
        }
    )

st.dataframe(
    ranking_table,
    width="stretch"
)


# =========================================================
# SAFE ROUTE RECOMMENDATION
# =========================================================

st.subheader("🛡️ Safe Route Recommendation")

best_route_result = recommend_best_route(
    route_data
)

best_route = best_route_result[
    "recommended_route"
]

st.success(
    f"Best Route: {best_route['name']}"
)

st.write(
    f"**Risk:** {best_route['risk_level']}"
)

st.write(
    f"**Distance:** "
    f"{best_route['distance_km']:.2f} km"
)

st.write(
    f"**Fuel Cost:** "
    f"₹{best_route['fuel_cost']:.2f}"
)

st.info(
    f"{best_route_result['message']} "
    f"{best_route_result['reason']}"
)


# =========================================================
# DYNAMIC RE-ROUTING
# =========================================================

st.subheader("🔄 Dynamic Re-Routing")

current_route = next(
    route
    for route in route_data
    if route["name"] == selected_route
)

current_route_data = {
    "name": selected_route,
    "distance_km": selected_distance,
    "risk_level": current_route["risk_level"],
    "ice_risk": current_route["ice_risk"],
    "fuel_cost": fuel_result["estimated_fuel_cost"]
}

alternative_routes = [
    route
    for route in route_data
    if route["name"] != selected_route
]

replan_result = replan_route(
    current_route_data,
    alternative_routes
)

if replan_result["status"] == "REPLANNED":

    st.success(
        f"Re-routing Recommended: "
        f"{replan_result['route']['name']}"
    )

    st.write(
        f"New Route Risk: "
        f"{replan_result['route']['calculated_risk']}"
    )

    st.write(
        f"New Route Distance: "
        f"{replan_result['route']['distance_km']:.2f} km"
    )

    st.write(
        replan_result["recommendation"]
    )

elif replan_result["status"] == "SAFE":

    st.success(
        "Current route is safe. "
        "No re-routing required."
    )

else:

    st.warning(
        replan_result["recommendation"]
    )


# =========================================================
# ANTARCTIC MONITORING MAP
# =========================================================

st.subheader("🗺️ Antarctic Monitoring Map")

# Small control area OUTSIDE the map
map_control_col, map_info_col = st.columns([1, 9])

with map_control_col:

    if st.session_state.map_expanded:

        if st.button(
            "↙ Close Map",
            key="close_map_button",
            use_container_width=True
        ):
            st.session_state.map_expanded = False
            st.rerun()

    else:

        if st.button(
            "⛶ Expand Map",
            key="expand_map_button",
            use_container_width=True
        ):
            st.session_state.map_expanded = True
            st.rerun()

with map_info_col:

    if st.session_state.map_expanded:

        st.caption(
            "🗺️ Expanded Antarctic monitoring map"
        )

    else:

        st.caption(
            "Map controls are outside the map"
        )


# =========================================================
# CREATE AND DISPLAY MAP
# =========================================================

try:

    antarctic_map = create_antarctic_map(
        start_name=start_location,
        start_coords=(start_lat, start_lon),
        destination_name=end_location,
        destination_coords=(end_lat, end_lon)
    )

    if st.session_state.map_expanded:

        st_folium(
            antarctic_map,
            width="stretch",
            height=700
        )

    else:

        st_folium(
    antarctic_map,
    width="stretch",
    height=700,
    key="antarctic_map_expanded"
)

except Exception as e:

    st.error(
        f"Map error: {e}"
    )


# =========================================================
# SYSTEM STATUS
# =========================================================

st.subheader("📡 System Status")

status_data = [
    {
        "Module": "Data Processing",
        "Status": "ONLINE"
    },
    {
        "Module": "AI Prediction",
        "Status": "ONLINE"
    },
    {
        "Module": "Risk Analysis",
        "Status": "ONLINE"
    },
    {
        "Module": "Route Optimization",
        "Status": "ONLINE"
    },
    {
        "Module": "Fuel Estimation",
        "Status": "ONLINE"
    },
    {
        "Module": "Dynamic Re-Routing",
        "Status": "ONLINE"
    },
    {
        "Module": "Antarctic Map",
        "Status": "ONLINE"
    }
]

st.dataframe(
    status_data,
    width="stretch"
)

st.success(
    "🟢 Antarctic AI Navigation System is ready for demonstration."
)
