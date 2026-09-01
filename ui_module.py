import streamlit as st


def show_route_card(route, selected=False):
    risk = route["risk"]

    if risk == "HIGH":
        risk_text = "🔴 HIGH RISK"
    elif risk == "MEDIUM":
        risk_text = "🟡 MEDIUM RISK"
    else:
        risk_text = "🟢 LOW RISK"

    if selected:
        st.success(f"⭐ SELECTED ROUTE — {route['name']}")

    st.subheader(route["name"])
    st.write(risk_text)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("📏 Distance", f"{route['distance_km']} km")
        st.metric("⛽ Fuel", f"{route['fuel_liters']} L")

    with col2:
        st.metric("💰 Fuel Cost", f"₹{route['fuel_cost']}")
        st.write(f"**Safety:** {risk}")

    st.divider()


def show_routes(
    routes,
    selected_route=None,
    recommended_route=None,
    replan_result=None
):
    st.title("🧊 Antarctic Navigation Dashboard")
    st.caption("Captain-friendly route overview")

    # AI Recommended Route
    if recommended_route:
        st.info(f"🤖 AI RECOMMENDED ROUTE: {recommended_route}")
    else:
        st.info("🤖 AI RECOMMENDED ROUTE: Not available")

    # Risk Alert
    # Risk Alert
    high_risk_routes = [
        route["name"]
        for route in routes
        if route["risk"] == "HIGH"
    ]

    medium_risk_routes = [
        route["name"]
        for route in routes
        if route["risk"] == "MEDIUM"
    ]

    if high_risk_routes:
        st.error(
            f"🔴 HIGH RISK ALERT: Avoid {', '.join(high_risk_routes)}"
        )
    elif medium_risk_routes:
        st.warning(
            f"🟡 MEDIUM RISK ALERT: Monitor {', '.join(medium_risk_routes)}"
        )
    else:
        st.success("🟢 RISK ALERT: No high or medium risk routes.")
   
    # Route Cards
    st.subheader("🛣️ Candidate Routes")

    for route in routes:
        selected = (
            selected_route is not None
            and route["name"] == selected_route
        )
        show_route_card(route, selected)

    # Safety vs Fuel Comparison
    st.subheader("⚖️ Safety vs Fuel Comparison")

    if len(routes) >= 2:
        for route in routes:
            st.write(
                f"**{route['name']}** — "
                f"Safety: {route['risk']} | "
                f"Fuel: {route['fuel_liters']} L | "
                f"Fuel Cost: ₹{route['fuel_cost']}"
            )
    else:
        st.info("At least two routes are required for comparison.")

    # Why this route?
    st.subheader("💡 Why this route?")

    if recommended_route:
        recommended_data = next(
            (
                route for route in routes
                if route["name"] == recommended_route
            ),
            None
        )

        if recommended_data:
            st.write(
                f"**{recommended_route}** is recommended because "
                f"its current risk is **{recommended_data['risk']}**, "
                f"with a distance of **{recommended_data['distance_km']} km** "
                f"and estimated fuel usage of "
                f"**{recommended_data['fuel_liters']} L**."
            )
        else:
            st.write("Recommendation details are not available.")
    else:
        st.write("No recommended route is available.")

    # Dynamic Re-routing
    st.subheader("🔄 Dynamic Re-routing")

    if replan_result:
        status = replan_result.get("status", "UNKNOWN")
        recommendation = replan_result.get(
            "recommendation",
            "No re-routing recommendation available."
        )
        route = replan_result.get("route")

        st.write(f"**Status:** {status}")
        st.write(f"**Recommendation:** {recommendation}")

        if route:
            st.success(
                f"🟢 Recommended Alternative: {route['name']}"
            )
        else:
            st.info("No alternative route available.")
    else:
        st.info("No re-routing result available.")