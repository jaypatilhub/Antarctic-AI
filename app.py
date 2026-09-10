import streamlit as st
import folium
from streamlit_folium import st_folium
from ai_prediction_module import get_ai_predictions
from risk_module import calculate_risk_from_data, get_risk_reason
from math import radians, sin, cos, sqrt, atan2


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Antarctic AI Navigation",
    page_icon="🧊"
)


# =========================================================
# TITLE
# =========================================================

st.title("🧊 Antarctic AI Navigation System")

st.write(
    "AI-based Antarctic Sea-Ice, "
    "Iceberg Trajectory and Navigation "
    "Decision Support System"
)

st.success("System Online")


# =========================================================
# AI PREDICTION ENGINE
# =========================================================

prediction_results = get_ai_predictions(days_ahead=3)

sea_ice_predictions = prediction_results["sea_ice_prediction"]

iceberg_predictions = prediction_results["iceberg_prediction"]


# =========================================================
# AI PREDICTION DISPLAY
# =========================================================

st.subheader("🧠 AI Prediction")

col1, col2 = st.columns(2)


# =========================================================
# SEA-ICE FORECAST
# =========================================================

with col1:

    st.write("🧊 Sea-Ice Forecast")

    for prediction in sea_ice_predictions:

        st.write(
            f"Day {prediction['day_ahead']}: "
            f"{prediction['predicted_sea_ice_concentration']}%"
        )


# =========================================================
# ICEBERG TRAJECTORY FORECAST
# =========================================================

with col2:

    st.write("🧊 Iceberg Trajectory Forecast")

    for prediction in iceberg_predictions:

        st.write(
            f"Day {prediction['day_ahead']}: "
            f"Lat {prediction['predicted_latitude']}, "
            f"Lon {prediction['predicted_longitude']}"
        )


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

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


# =========================================================
# VESSEL / RESEARCH POINT
# =========================================================

vessel_latitude = -75.0
vessel_longitude = 0.0


# =========================================================
# RISK ANALYSIS
# =========================================================

st.subheader("⚠️ AI Risk Analysis")

risk_results = []

for iceberg, sea_ice in zip(
    iceberg_predictions,
    sea_ice_predictions
):

    iceberg_lat = iceberg["predicted_latitude"]
    iceberg_lon = iceberg["predicted_longitude"]

    sea_ice_concentration = (
        sea_ice["predicted_sea_ice_concentration"]
    )

    distance = calculate_distance_km(
        vessel_latitude,
        vessel_longitude,
        iceberg_lat,
        iceberg_lon
    )

    risk = calculate_risk_from_data(
        distance,
        sea_ice_concentration
    )

    reason = get_risk_reason(distance)

    risk_results.append({
        "day": iceberg["day_ahead"],
        "distance": round(distance, 2),
        "sea_ice": sea_ice_concentration,
        "risk": risk,
        "reason": reason
    })


# =========================================================
# DISPLAY RISK
# =========================================================

for result in risk_results:

    st.write(
        f"**Day {result['day']}** → "
        f"Risk: **{result['risk']}** | "
        f"Distance: {result['distance']} km | "
        f"Sea-Ice: {result['sea_ice']}%"
    )

    st.caption(result["reason"])


# =========================================================
# MAP
# =========================================================

st.subheader("🗺️ Antarctic AI Prediction Map")

m = folium.Map(
    location=[-75, 20],
    zoom_start=3,
    tiles="OpenStreetMap"
)


# =========================================================
# VESSEL / RESEARCH POINT
# =========================================================

folium.CircleMarker(
    location=[
        vessel_latitude,
        vessel_longitude
    ],
    radius=8,
    popup="Antarctic Research Vessel",
    tooltip="Research Vessel",
    fill=True
).add_to(m)


# =========================================================
# AI RISK ZONE
# =========================================================

folium.Circle(
    location=[-72, 20],
    radius=500000,
    popup="AI Risk Zone",
    tooltip="AI Risk Zone",
    fill=True
).add_to(m)


# =========================================================
# AI PREDICTED ICEBERG POSITIONS
# =========================================================

predicted_points = []

for iceberg in iceberg_predictions:

    lat = iceberg["predicted_latitude"]
    lon = iceberg["predicted_longitude"]
    day = iceberg["day_ahead"]
    speed = iceberg["speed_kmh"]
    direction = iceberg["direction"]

    predicted_points.append([lat, lon])

    # Find matching risk result
    matching_risk = next(
        item for item in risk_results
        if item["day"] == day
    )

    risk = matching_risk["risk"]

    folium.CircleMarker(
        location=[lat, lon],
        radius=9,
        popup=(
            f"AI Predicted Iceberg - Day {day}<br>"
            f"Latitude: {lat}<br>"
            f"Longitude: {lon}<br>"
            f"Speed: {speed} km/h<br>"
            f"Direction: {direction}<br>"
            f"Risk: {risk}"
        ),
        tooltip=(
            f"Day {day} | Risk: {risk}"
        ),
        fill=True
    ).add_to(m)


# =========================================================
# AI PREDICTED TRAJECTORY
# =========================================================

if len(predicted_points) > 1:

    folium.PolyLine(
        locations=predicted_points,
        weight=4,
        tooltip="AI Predicted Iceberg Trajectory"
    ).add_to(m)


# =========================================================
# DISPLAY MAP
# =========================================================

st_folium(
    m,
    width=900,
    height=600
)