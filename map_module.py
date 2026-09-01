import folium


def create_antarctic_map():

    # =========================================================
    # GLOBAL WORLD MAP
    # =========================================================

    map_obj = folium.Map(
        location=[20, 0],
        zoom_start=2,
        min_zoom=2,
        max_zoom=8,
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
        box-shadow: 0 0 15px #00eaff;
    ">
        🌍 ANTARCTIC AI — GLOBAL VESSEL MONITOR
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(title_html)
    )

    # =========================================================
    # LEFT PANEL
    # =========================================================

    info_panel = """
    <div style="
        position: fixed;
        top: 80px;
        left: 20px;
        z-index: 9999;
        width: 230px;
        background: rgba(5, 15, 25, 0.95);
        color: white;
        padding: 15px;
        border: 1px solid #00eaff;
        border-radius: 10px;
        font-family: Arial;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">

        <div style="
            color:#00eaff;
            font-size:17px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            🧠 AI STATUS
        </div>

        <div>🟢 SYSTEM: ONLINE</div>
        <div>🟢 VESSEL MONITORING: ACTIVE</div>
        <div>🟢 ICE ANALYSIS: ACTIVE</div>

        <hr style="border-color:#24404a;">

        <div style="color:#00eaff;">
            🚢 GLOBAL VESSELS
        </div>

        <div>Tracked Vessels: 06</div>
        <div>Our Vessel: 01</div>
        <div>Other Vessels: 05</div>

        <hr style="border-color:#24404a;">

        <div style="color:#00eaff;">
            🧊 ANTARCTIC DATA
        </div>

        <div>Icebergs: 03</div>
        <div>Risk Zone: ACTIVE</div>

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(info_panel)
    )

    # =========================================================
    # RIGHT LEGEND
    # =========================================================

    legend_html = """
    <div style="
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 9999;
        width: 190px;
        background: rgba(5, 15, 25, 0.95);
        color: white;
        padding: 15px;
        border: 1px solid #00eaff;
        border-radius: 10px;
        font-family: Arial;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">

        <div style="
            color:#00eaff;
            font-size:17px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            🗺️ MAP LEGEND
        </div>

        <div>🚢 Our Ship</div>
        <div>🚢 Other Vessel</div>
        <div>🧊 Iceberg</div>
        <div>🟢 Low Ice</div>
        <div>🟡 Medium Ice</div>
        <div>🔴 Heavy Ice</div>
        <div>🔴 Route A — HIGH RISK</div>
        <div>🟡 Route B — MEDIUM RISK</div>
        <div>🟢 Route C — LOW RISK</div>
        <div>⚠️ AI Risk Zone</div>
        <div>🏁 Destination</div>

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
        location=[-70, 20],
        popup="""
        <div style="font-family:Arial; width:230px;">

            <h4 style="color:#0088aa;">
                🚢 OUR RESEARCH SHIP
            </h4>

            <b>Latitude:</b> -70°<br>
            <b>Longitude:</b> 20°<br>
            <b>Speed:</b> 12.0 knots<br>
            <b>Heading:</b> 074°<br>
            <b>Destination:</b> Antarctic Research Station<br>
            <b>Status:</b> 🟢 ACTIVE<br>
            <b>AI Risk:</b> 🔴 HIGH

        </div>
        """,
        tooltip="🚢 OUR RESEARCH SHIP",
        icon=ship_icon
    ).add_to(map_obj)

    # =========================================================
    # AI MONITORING RANGE
    # =========================================================

    radar_center = [-70, 20]

    folium.Circle(
        location=radar_center,
        radius=150000,
        color="#00eaff",
        weight=2,
        fill=False,
        tooltip="🛰️ AI Monitoring Range"
    ).add_to(map_obj)

    folium.Circle(
        location=radar_center,
        radius=300000,
        color="#00eaff",
        weight=1,
        fill=False
    ).add_to(map_obj)

    folium.Circle(
        location=radar_center,
        radius=450000,
        color="#00eaff",
        weight=1,
        fill=False
    ).add_to(map_obj)

    # =========================================================
    # LOW ICE
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

    # =========================================================
    # MEDIUM ICE
    # =========================================================

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

    # =========================================================
    # HEAVY ICE
    # =========================================================

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
    # AI RISK ZONE
    # =========================================================

    folium.Circle(
        location=[-72, 20],
        radius=500000,
        popup="⚠️ AI High Risk Zone",
        tooltip="⚠️ AI HIGH RISK AREA",
        color="#ff0033",
        weight=2,
        fill=True,
        fill_color="#ff0033",
        fill_opacity=0.12
    ).add_to(map_obj)
    # =========================================================
    # START LOCATION
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
        location=[-70, 20],
        popup="""
        <b>START LOCATION</b><br>
        Our Vessel Starting Point<br>
        Latitude: -70°<br>
        Longitude: 20°
        """,
        tooltip="START",
        icon=start_icon
    ).add_to(map_obj)

    # =========================================================
    # DESTINATION
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
        location=[-68, 30],
        popup="""
        <b>🏁 RESEARCH DESTINATION</b><br>
        Target: Antarctic Research Station<br>
        Navigation Status: ACTIVE
        """,
        tooltip="🏁 DESTINATION",
        icon=destination_icon
    ).add_to(map_obj)
    # =========================================================
# =========================================================
    # ROUTE SELECTION
    # =========================================================

    route_layer = folium.FeatureGroup(name="🗺️ Routes")
    route_layer.add_to(map_obj)

    # =========================================================
    # ROUTE A — HIGH RISK
    # =========================================================

    folium.PolyLine(
        locations=[
            [-70, 20],
            [-69.5, 21],
            [-69, 23],
            [-68.5, 26],
            [-68, 30]
        ],
        color="#ff2222",
        weight=5,
        opacity=0.85,
        tooltip="Route A — HIGH RISK"
    ).add_to(route_layer)
    # =========================================================
    # ROUTE B — MEDIUM RISK
    # =========================================================

    folium.PolyLine(
        locations=[
            [-70, 20],
            [-69.8, 22],
            [-69.5, 24],
            [-69, 27],
            [-68, 30]
        ],
        color="#ffaa00",
        weight=5,
        opacity=0.85,
        tooltip="Route B — MEDIUM RISK"
    ).add_to(route_layer)
    # =========================================================
    # ROUTE C — LOW RISK
    # =========================================================

    folium.PolyLine(
        locations=[
            [-70, 20],
            [-70.2, 21.5],
            [-69.8, 24],
            [-69, 27],
            [-68, 30]
        ],
        color="#00cc55",
        weight=5,
        opacity=0.85,
        tooltip="Route C — LOW RISK"
    ).add_to(route_layer)

    # =========================================================
    # AI RECOMMENDED ROUTE
    # =========================================================

    folium.PolyLine(
        locations=[
            [-70, 20],
            [-69.5, 22],
            [-69, 24],
            [-68.5, 27],
            [-68, 30]
        ],
        color="#00eaff",
        weight=4,
        opacity=0.9,
        dash_array="10, 8",
        tooltip="🛰️ AI RECOMMENDED ROUTE"
    ).add_to(map_obj)

    # =========================================================
    # ICEBERG ICON
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

    # =========================================================
    # ICEBERG 01
    # =========================================================

    folium.Marker(
        location=[-71, 25],
        popup="""
        <b>🧊 ICEBERG 01</b><br>
        Location: -71°, 25°<br>
        Size: Large<br>
        Movement: South-East<br>
        Risk: <b style="color:red;">HIGH</b>
        """,
        tooltip="🧊 ICEBERG 01 — HIGH RISK",
        icon=iceberg_icon
    ).add_to(map_obj)

    folium.PolyLine(
        locations=[
            [-71, 25],
            [-70.5, 26],
            [-70, 27]
        ],
        color="#ff2222",
        weight=4,
        tooltip="➡️ Iceberg 01 Movement"
    ).add_to(map_obj)

    # =========================================================
    # ICEBERG 02
    # =========================================================

    folium.Marker(
        location=[-73, 15],
        popup="""
        <b>🧊 ICEBERG 02</b><br>
        Location: -73°, 15°<br>
        Size: Medium<br>
        Movement: East<br>
        Risk: <b style="color:orange;">MEDIUM</b>
        """,
        tooltip="🧊 ICEBERG 02 — MEDIUM RISK",
        icon=iceberg_icon
    ).add_to(map_obj)

    folium.PolyLine(
        locations=[
            [-73, 15],
            [-73, 17],
            [-73, 19]
        ],
        color="#ffaa00",
        weight=4,
        tooltip="➡️ Iceberg 02 Movement"
    ).add_to(map_obj)

    # =========================================================
    # ICEBERG 03
    # =========================================================

    folium.Marker(
        location=[-75, 28],
        popup="""
        <b>🧊 ICEBERG 03</b><br>
        Location: -75°, 28°<br>
        Size: Large<br>
        Movement: South<br>
        Risk: <b style="color:red;">HIGH</b>
        """,
        tooltip="🧊 ICEBERG 03 — HIGH RISK",
        icon=iceberg_icon
    ).add_to(map_obj)

    folium.PolyLine(
        locations=[
            [-75, 28],
            [-76, 28],
            [-77, 28]
        ],
        color="#ff2222",
        weight=4,
        tooltip="⬇️ Iceberg 03 Movement"
    ).add_to(map_obj)

    # =========================================================
    # GLOBAL WORLD VIEW
    # =========================================================
    # This forces the map to show the complete world initially.

    map_obj.fit_bounds(
        [
            [-60, -170],
            [80, 170]
        ]
    )

    # =========================================================
    # BOTTOM STATUS BAR
    # =========================================================

    status_bar = """
    <div style="
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background: rgba(5,15,25,0.95);
        color: #00eaff;
        padding: 10px 25px;
        border: 1px solid #00eaff;
        border-radius: 8px;
        font-family: Arial;
        font-size: 14px;
        box-shadow: 0 0 12px rgba(0,234,255,0.5);
    ">
        🌍 GLOBAL VESSEL MONITORING: ONLINE
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🧠 AI ENGINE: ACTIVE
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🧊 ICE MONITORING: ACTIVE
        &nbsp;&nbsp;|&nbsp;&nbsp;
        🚢 NAVIGATION: ACTIVE
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(status_bar)
    )
# =========================================================
    # ROUTE SELECTION CONTROL
    # =========================================================

    folium.LayerControl(
        collapsed=False
    ).add_to(map_obj)

    return map_obj