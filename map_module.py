import folium
from folium.plugins import Fullscreen


def create_antarctic_map(
    start_name="Our Research Ship",
    start_coords=(-70, 20),
    destination_name="Antarctic Research Station",
    destination_coords=(-68, 30),
):
    start_lat, start_lon = start_coords
    destination_lat, destination_lon = destination_coords

    start_point = [start_lat, start_lon]
    destination_point = [destination_lat, destination_lon]

    map_obj = folium.Map(
    location=(-75, 20),
    zoom_start=4,
    tiles="OpenStreetMap"
)

    # =========================================================
    # TITLE
    # =========================================================

    title_html = """
    <div style="
        position: fixed;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background: rgba(5, 15, 25, 0.95);
        color: #00eaff;
        padding: 12px 30px;
        border: 1px solid #00eaff;
        border-radius: 8px;
        font-family: Arial;
        font-size: 22px;
        font-weight: bold;
        letter-spacing: 2px;
        white-space: nowrap;
        box-shadow: 0 0 15px #00eaff;
    ">
        ANTARCTIC AI — GLOBAL VESSEL MONITOR
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(title_html)
    )

    # =========================================================
    # LEFT AI STATUS PANEL
    # =========================================================

    info_panel = """
    <div style="
        position: fixed;
        top: 80px;
        left: 20px;
        z-index: 9999;
        width: 230px;
        max-width: 24vw;
        background: rgba(5, 15, 25, 0.95);
        color: white;
        padding: 15px;
        border: 1px solid #00eaff;
        border-radius: 10px;
        font-family: Arial;
        font-size: 13px;
        line-height: 1.5;
        box-sizing: border-box;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">
        <div style="
            color:#00eaff;
            font-size:17px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            AI STATUS
        </div>

        <div>🟢 SYSTEM: ONLINE</div>
        <div>🟢 VESSEL MONITORING: ACTIVE</div>
        <div>🟢 ICE ANALYSIS: ACTIVE</div>
        <div>🟢 WEATHER MONITORING: ACTIVE</div>
        <div>🟢 OCEAN MONITORING: ACTIVE</div>

        <hr style="border-color:#24404a;">

        <div style="color:#00eaff;">
            GLOBAL VESSELS
        </div>

        <div>Tracked Vessels: 06</div>
        <div>Our Vessel: 01</div>
        <div>Other Vessels: 05</div>

        <hr style="border-color:#24404a;">

        <div style="color:#00eaff;">
            ANTARCTIC DATA
        </div>

        <div>Icebergs: 03</div>
        <div>Risk Zone: ACTIVE</div>
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(info_panel)
    )

    # =========================================================
    # RIGHT MAP LEGEND
    # =========================================================

    legend_html = """
    <div style="
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 9999;
        width: 205px;
        max-width: 22vw;
        background: rgba(5, 15, 25, 0.95);
        color: white;
        padding: 15px;
        border: 1px solid #00eaff;
        border-radius: 10px;
        font-family: Arial;
        font-size: 13px;
        line-height: 1.5;
        box-sizing: border-box;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">
        <div style="
            color:#00eaff;
            font-size:17px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            MAP LEGEND
        </div>

        <div>🚢 Our Ship</div>
        <div>⛴ Other Vessel</div>
        <div>🧊 Iceberg</div>
        <div>🟢 Low Ice</div>
        <div>🟡 Medium Ice</div>
        <div>🔴 Heavy Ice</div>
        <div>🔴 Route A — HIGH RISK</div>
        <div>🟡 Route B — MEDIUM RISK</div>
        <div>🟢 Route C — LOW RISK</div>
        <div>🔵 AI Recommended Route</div>
        <div>⚠️ AI Risk Zone</div>
        <div>🏁 Destination</div>
        <div>🌦️ Weather</div>
        <div>🌊 Ocean Current</div>
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(legend_html)
    )

    # =========================================================
    # GLOBAL DEMO SHIPS
    # =========================================================

    vessel_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:25px;
            text-align:center;
            width:35px;
            height:35px;
        ">
            ⛴
        </div>
        """
    )

    vessels = [
        {
            "name": "Ocean Pioneer",
            "type": "Research Vessel",
            "lat": 15,
            "lon": 20,
            "speed": "12.4 knots",
            "heading": "074°",
            "destination": "Cape Town",
            "status": "Active"
        },
        {
            "name": "Polar Explorer",
            "type": "Research Vessel",
            "lat": -35,
            "lon": 35,
            "speed": "10.8 knots",
            "heading": "120°",
            "destination": "Antarctica",
            "status": "Active"
        },
        {
            "name": "Southern Star",
            "type": "Cargo Vessel",
            "lat": -45,
            "lon": 70,
            "speed": "14.2 knots",
            "heading": "210°",
            "destination": "Hobart",
            "status": "Active"
        },
        {
            "name": "Atlantic Voyager",
            "type": "Supply Vessel",
            "lat": 10,
            "lon": -30,
            "speed": "16.1 knots",
            "heading": "095°",
            "destination": "South America",
            "status": "Active"
        },
        {
            "name": "Ice Navigator",
            "type": "Ice Research Vessel",
            "lat": -55,
            "lon": 20,
            "speed": "9.5 knots",
            "heading": "180°",
            "destination": "Antarctica",
            "status": "Active"
        }
    ]

    for vessel in vessels:

        popup_html = f"""
        <div style="font-family:Arial; width:230px;">
            <h4 style="color:#0088aa;">
                🚢 {vessel["name"]}
            </h4>

            <b>Vessel Type:</b> {vessel["type"]}<br>
            <b>Latitude:</b> {vessel["lat"]}°<br>
            <b>Longitude:</b> {vessel["lon"]}°<br>
            <b>Speed:</b> {vessel["speed"]}<br>
            <b>Heading:</b> {vessel["heading"]}<br>
            <b>Destination:</b> {vessel["destination"]}<br>
            <b>AIS Status:</b> 🟢 {vessel["status"]}
        </div>
        """

        folium.Marker(
            location=[vessel["lat"], vessel["lon"]],
            popup=folium.Popup(
                popup_html,
                max_width=300
            ),
            tooltip=f'🚢 {vessel["name"]}',
            icon=vessel_icon
        ).add_to(map_obj)

    # =========================================================
    # OUR RESEARCH SHIP
    # =========================================================

    ship_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:35px;
            text-align:center;
            width:45px;
            height:45px;
            filter: drop-shadow(0 0 10px #00eaff);
        ">
            🚢
        </div>
        """
    )

    folium.Marker(
        location=start_point,
        popup=f"""
        <div style="font-family:Arial; width:250px;">
            <h4 style="color:#0088aa;">
                🚢 OUR RESEARCH SHIP
            </h4>

            <b>Start Point:</b> {start_name}<br>
            <b>Latitude:</b> {start_lat:.4f}°<br>
            <b>Longitude:</b> {start_lon:.4f}°<br>
            <b>Destination:</b> {destination_name}<br>
            <b>Status:</b> 🟢 ACTIVE
        </div>
        """,
        tooltip=f"🚢 START: {start_name}",
        icon=ship_icon
    ).add_to(map_obj)

    # =========================================================
    # AI MONITORING RANGE
    # =========================================================

    for radius, weight in [
        (150000, 2),
        (300000, 1),
        (450000, 1)
    ]:

        folium.Circle(
            location=start_point,
            radius=radius,
            color="#00eaff",
            weight=weight,
            fill=False,
            tooltip="AI Monitoring Range"
            if radius == 150000 else None
        ).add_to(map_obj)

    # =========================================================
    # SEA-ICE ZONES
    # =========================================================

    low_ice_zone = [
        [-66, 5],
        [-65, 18],
        [-67, 28],
        [-69, 30],
        [-70, 18],
        [-69, 7]
    ]

    folium.Polygon(
        locations=low_ice_zone,
        popup="🟢 Low Sea-Ice Concentration",
        tooltip="🟢 LOW ICE",
        color="#00ff66",
        weight=2,
        fill=True,
        fill_color="#00ff66",
        fill_opacity=0.20
    ).add_to(map_obj)

    medium_ice_zone = [
        [-70, 5],
        [-69, 18],
        [-71, 32],
        [-74, 35],
        [-75, 25],
        [-74, 10]
    ]

    folium.Polygon(
        locations=medium_ice_zone,
        popup="🟡 Medium Sea-Ice Concentration",
        tooltip="🟡 MEDIUM ICE",
        color="#ffaa00",
        weight=2,
        fill=True,
        fill_color="#ffaa00",
        fill_opacity=0.25
    ).add_to(map_obj)

    heavy_ice_zone = [
        [-74, 10],
        [-73, 25],
        [-75, 35],
        [-78, 30],
        [-79, 15],
        [-77, 5]
    ]

    folium.Polygon(
        locations=heavy_ice_zone,
        popup="🔴 Heavy Sea-Ice Concentration",
        tooltip="🔴 HEAVY ICE",
        color="#ff2222",
        weight=2,
        fill=True,
        fill_color="#ff2222",
        fill_opacity=0.30
    ).add_to(map_obj)

    # =========================================================
    # AI HIGH RISK ZONE
    # =========================================================

    folium.Circle(
        location=[-72, 20],
        radius=500000,
        popup="""
        <b>⚠️ AI HIGH RISK ZONE</b><br><br>

        <b>Risk Factors:</b><br>
        • Heavy Sea-Ice<br>
        • Iceberg Activity<br>
        • Environmental Conditions<br><br>

        <b>Navigation Advice:</b><br>
        Prefer safer route alternatives.
        """,
        tooltip="⚠️ AI HIGH RISK AREA",
        color="#ff0033",
        weight=2,
        fill=True,
        fill_color="#ff0033",
        fill_opacity=0.12
    ).add_to(map_obj)

    # =========================================================
    # WEATHER INFORMATION — M6
    # =========================================================

    weather_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:25px;
            text-align:center;
            width:40px;
            height:40px;
        ">
            🌦️
        </div>
        """
    )

    weather_popup = """
    <div style="font-family:Arial; width:250px;">
        <h4 style="color:#0088aa;">
            🌦️ WEATHER INFORMATION
        </h4>

        <b>Data Status:</b>
        <span style="color:#d97706;">
            DEMO / SIMULATION
        </span><br><br>

        <b>Temperature:</b> -8°C<br>
        <b>Wind Speed:</b> 18 knots<br>
        <b>Wind Direction:</b> 074°<br>
        <b>Visibility:</b> 6 km<br>
        <b>Condition:</b> Partly Cloudy<br><br>

        <b>Navigation Impact:</b>
        Moderate
    </div>
    """

    folium.Marker(
        location=[-68, 25],
        popup=folium.Popup(
            weather_popup,
            max_width=320
        ),
        tooltip="🌦️ Weather Information",
        icon=weather_icon
    ).add_to(map_obj)

    # =========================================================
    # OCEAN CURRENT INFORMATION — M6
    # =========================================================

    ocean_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:25px;
            text-align:center;
            width:40px;
            height:40px;
        ">
            🌊
        </div>
        """
    )

    ocean_popup = """
    <div style="font-family:Arial; width:250px;">
        <h4 style="color:#0088aa;">
            🌊 OCEAN CURRENT
        </h4>

        <b>Data Status:</b>
        <span style="color:#d97706;">
            DEMO / SIMULATION
        </span><br><br>

        <b>Current Speed:</b> 0.8 m/s<br>
        <b>Current Direction:</b> 135°<br>
        <b>Flow:</b> South-East<br>
        <b>Navigation Impact:</b> Moderate<br><br>

        Ocean conditions are considered
        during route analysis.
    </div>
    """

    folium.Marker(
        location=[-69, 30],
        popup=folium.Popup(
            ocean_popup,
            max_width=320
        ),
        tooltip="🌊 Ocean Current Information",
        icon=ocean_icon
    ).add_to(map_obj)

    # =========================================================
    # SELECTED START MARKER
    # =========================================================

    start_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:28px;
            text-align:center;
            width:40px;
            height:40px;
            filter: drop-shadow(0 0 8px #00eaff);
        ">
            📍
        </div>
        """
    )

    folium.Marker(
        location=start_point,
        popup=f"""
        <b>START LOCATION</b><br>
        {start_name}<br>
        Latitude: {start_lat:.4f}°<br>
        Longitude: {start_lon:.4f}°
        """,
        tooltip=f"START: {start_name}",
        icon=start_icon
    ).add_to(map_obj)

    # =========================================================
    # SELECTED DESTINATION MARKER
    # =========================================================

    destination_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:30px;
            text-align:center;
            width:40px;
            height:40px;
            filter: drop-shadow(0 0 8px #00ff66);
        ">
            🏁
        </div>
        """
    )

    folium.Marker(
        location=destination_point,
        popup=f"""
        <b>🏁 RESEARCH DESTINATION</b><br>
        {destination_name}<br>
        Latitude: {destination_lat:.4f}°<br>
        Longitude: {destination_lon:.4f}°<br>
        Navigation Status: ACTIVE
        """,
        tooltip=f"🏁 DESTINATION: {destination_name}",
        icon=destination_icon
    ).add_to(map_obj)

    # =========================================================
    # ROUTE CALCULATION
    # =========================================================

    lat_difference = destination_lat - start_lat
    lon_difference = destination_lon - start_lon

    def route_points(offset):
        return [
            start_point,
            [
                start_lat + (lat_difference * 0.33) + offset,
                start_lon + (lon_difference * 0.33)
            ],
            [
                start_lat + (lat_difference * 0.66) + offset,
                start_lon + (lon_difference * 0.66)
            ],
            destination_point
        ]

    # =========================================================
    # ROUTES
    # =========================================================

    route_layer = folium.FeatureGroup(
        name="🗺️ Routes"
    )

    route_layer.add_to(map_obj)

    route_a_points = route_points(0.7)
    route_b_points = route_points(0.0)
    route_c_points = route_points(-0.7)
    recommended_route_points = route_points(-0.25)

    # ROUTE A
    route_a_popup = """
    <div style="font-family:Arial; width:250px;">
        <h4 style="color:#cc2222;">
            🔴 ROUTE A — HIGH RISK
        </h4>

        <b>Risk Level:</b> HIGH<br>
        <b>Sea-Ice:</b> Heavy<br>
        <b>Iceberg Exposure:</b> High<br>
        <b>Weather Impact:</b> Moderate<br>
        <b>Navigation:</b> Not Preferred<br><br>

        AI recommends checking safer alternatives.
    </div>
    """

    folium.PolyLine(
        locations=route_a_points,
        color="#ff2222",
        weight=5,
        opacity=0.85,
        tooltip="Route A — HIGH RISK",
        popup=folium.Popup(
            route_a_popup,
            max_width=320
        )
    ).add_to(route_layer)

    # ROUTE B
    route_b_popup = """
    <div style="font-family:Arial; width:250px;">
        <h4 style="color:#cc8800;">
            🟡 ROUTE B — MEDIUM RISK
        </h4>

        <b>Risk Level:</b> MEDIUM<br>
        <b>Sea-Ice:</b> Moderate<br>
        <b>Iceberg Exposure:</b> Medium<br>
        <b>Weather Impact:</b> Moderate<br>
        <b>Navigation:</b> Acceptable<br><br>

        Balanced option between safety and distance.
    </div>
    """

    folium.PolyLine(
        locations=route_b_points,
        color="#ffaa00",
        weight=5,
        opacity=0.85,
        tooltip="Route B — MEDIUM RISK",
        popup=folium.Popup(
            route_b_popup,
            max_width=320
        )
    ).add_to(route_layer)

    # ROUTE C
    route_c_popup = """
    <div style="font-family:Arial; width:250px;">
        <h4 style="color:#008844;">
            🟢 ROUTE C — LOW RISK
        </h4>

        <b>Risk Level:</b> LOW<br>
        <b>Sea-Ice:</b> Lower<br>
        <b>Iceberg Exposure:</b> Lower<br>
        <b>Weather Impact:</b> Lower<br>
        <b>Navigation:</b> Preferred<br><br>

        Safer route option for navigation.
    </div>
    """

    folium.PolyLine(
        locations=route_c_points,
        color="#00cc55",
        weight=5,
        opacity=0.85,
        tooltip="Route C — LOW RISK",
        popup=folium.Popup(
            route_c_popup,
            max_width=320
        )
    ).add_to(route_layer)

    # =========================================================
    # AI RECOMMENDED ROUTE
    # =========================================================

    ai_route_popup = """
    <div style="font-family:Arial; width:270px;">
        <h4 style="color:#0088aa;">
            🛰️ AI RECOMMENDED ROUTE
        </h4>

        <b>Recommendation:</b> Preferred<br>
        <b>Safety Priority:</b> High<br>
        <b>Ice Risk:</b> Low / Moderate<br>
        <b>Iceberg Risk:</b> Monitored<br>
        <b>Weather:</b> Monitored<br>
        <b>Ocean Conditions:</b> Considered<br><br>

        AI selects the route by balancing
        safety and navigation efficiency.
    </div>
    """

    folium.PolyLine(
        locations=recommended_route_points,
        color="#00eaff",
        weight=4,
        opacity=0.9,
        dash_array="10, 8",
        tooltip="🛰️ AI RECOMMENDED ROUTE",
        popup=folium.Popup(
            ai_route_popup,
            max_width=330
        )
    ).add_to(map_obj)

    # =========================================================
    # ICEBERG DATA
    # =========================================================

    iceberg_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:28px;
            text-align:center;
            width:40px;
            height:40px;
        ">
            🧊
        </div>
        """
    )

    icebergs = [
        {
            "name": "ICEBERG 01",
            "location": [-69, 23],
            "size": "Large",
            "movement": "South-East",
            "risk": "HIGH",
            "risk_color": "red",
            "path": [
                [-69, 23],
                [-70.5, 26],
                [-70, 27]
            ],
            "path_color": "#ff2222"
        },
        {
            "name": "ICEBERG 02",
            "location": [-73, 15],
            "size": "Medium",
            "movement": "East",
            "risk": "MEDIUM",
            "risk_color": "orange",
            "path": [
                [-73, 15],
                [-73, 17],
                [-73, 19]
            ],
            "path_color": "#ffaa00"
        },
        {
            "name": "ICEBERG 03",
            "location": [-75, 28],
            "size": "Large",
            "movement": "South",
            "risk": "HIGH",
            "risk_color": "red",
            "path": [
                [-75, 28],
                [-76, 28],
                [-77, 28]
            ],
            "path_color": "#ff2222"
        }
    ]

    for iceberg in icebergs:

        iceberg_popup = f"""
        <div style="font-family:Arial; width:270px;">

            <h4 style="color:#0088aa;">
                🧊 {iceberg["name"]}
            </h4>

            <b>Current Location:</b>
            {iceberg["location"][0]}°,
            {iceberg["location"][1]}°<br>

            <b>Size:</b> {iceberg["size"]}<br>
            <b>Predicted Movement:</b> {iceberg["movement"]}<br>

            <b>Risk Level:</b>
            <span style="color:{iceberg["risk_color"]};">
                {iceberg["risk"]}
            </span>

            <hr>

            <b>⚠️ Navigation Warning</b><br>

            This iceberg is being monitored by
            the navigation system.<br><br>

            <b>Trajectory Status:</b> ACTIVE<br>
            <b>Collision Monitoring:</b> ACTIVE<br>
            <b>Route Impact:</b>
            {"HIGH" if iceberg["risk"] == "HIGH" else "MODERATE"}
        </div>
        """

        folium.Marker(
            location=iceberg["location"],
            popup=folium.Popup(
                iceberg_popup,
                max_width=340
            ),
            tooltip=f"🧊 {iceberg['name']} — {iceberg['risk']} RISK",
            icon=iceberg_icon
        ).add_to(map_obj)

        folium.PolyLine(
            locations=iceberg["path"],
            color=iceberg["path_color"],
            weight=4,
            tooltip=f"➡️ {iceberg['name']} Movement"
        ).add_to(map_obj)

    # =========================================================
    # NAVIGATION-FOCUSED MAP VIEW
    # =========================================================

    if start_point != destination_point:

        map_obj.fit_bounds(
            [start_point, destination_point],
            padding=(70, 70)
        )

    # =========================================================
    # BOTTOM STATUS BAR
    # =========================================================

    status_bar = f"""
    <div style="
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        max-width: 90%;
        background: rgba(5,15,25,0.95);
        color: #00eaff;
        padding: 10px 25px;
        border: 1px solid #00eaff;
        border-radius: 8px;
        font-family: Arial;
        font-size: 14px;
        text-align: center;
        box-sizing: border-box;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">
        🚢 ROUTE: {start_name} → {destination_name}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🧊 ICE MONITORING: ACTIVE
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🌦️ WEATHER: MONITORED
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🌊 OCEAN: MONITORED
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🧭 NAVIGATION: ACTIVE
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(status_bar)
    )

    # =========================================================
    # FULLSCREEN CONTROL
    # =========================================================

    Fullscreen(
        position="topleft",
        title="Open Fullscreen",
        title_cancel="Exit Fullscreen",
        force_separate_button=True
    ).add_to(map_obj)

    # =========================================================
    # LAYER CONTROL
    # =========================================================

    folium.LayerControl(
        collapsed=False
    ).add_to(map_obj)

    return map_obj