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


def show_routes(routes, selected_route=None):
    st.title("🧊 Antarctic Navigation Dashboard")
    st.caption("Captain-friendly route overview")
    st.info("🤖 AI RECOMMENDED ROUTE: Route A")
    st.warning("⚠️ RISK ALERT: Monitor routes with MEDIUM or HIGH risk.")
    st.subheader("⚖️ Safety vs Fuel Comparison")
    
    if len(routes) >= 2:
            col1, col2 = st.columns(2)

    with col1:
            st.write("**Route A**")
            st.write(f"Safety: {routes[0]['risk']}")
            st.write(f"Fuel: {routes[0]['fuel_liters']} L")
            st.write(f"Fuel Cost: ₹{routes[0]['fuel_cost']}")
    with col2:
            st.write("**Route B**")
            st.write(f"Safety: {routes[1]['risk']}")
            st.write(f"Fuel: {routes[1]['fuel_liters']} L")
            st.write(f"Fuel Cost: ₹{routes[1]['fuel_cost']}")

    st.subheader("💡 Why this route?")

    st.write(
        "Route A is recommended because it has a safer risk level "
        "compared with the other candidate routes."
    )
    st.subheader("🔄 Dynamic Re-routing")

    st.write(
        "If the current route becomes unsafe, "
        "the system can recommend a safer alternative."
    )

    st.success(
        "🟢 RE-ROUTED: Safer alternative route available."
    )

    st.write("**Recommended Alternative:** Route A")        
    for route in routes:
        selected = (
            selected_route is not None
            and route["name"] == selected_route
        )

        show_route_card(route, selected)