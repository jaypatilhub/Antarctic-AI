import folium


def create_antarctic_map():

    # =========================================================
    # MAIN WORLD MAP
    # =========================================================

    map_obj = folium.Map(
        location=[10, 0],
        zoom_start=2,
        min_zoom=2,
        max_zoom=10,
        tiles=None,
        control_scale=True
    )

    # =========================================================
    # BASE MAPS
    # =========================================================

    folium.TileLayer(
        "OpenStreetMap",
        name="🌍 OpenStreetMap",
        control=True
    ).add_to(map_obj)

    folium.TileLayer(
        "CartoDB dark_matter",
        name="🌑 Dark Surveillance",
        control=True
    ).add_to(map_obj)

    # =========================================================
    # TITLE
    # =========================================================

    title_html = """
    <div style="
        position:fixed;
        top:12px;
        left:50%;
        transform:translateX(-50%);
        z-index:5000;

        background:rgba(5,15,25,0.96);
        color:#00eaff;

        padding:10px 25px;
        border:1px solid #00eaff;
        border-radius:8px;

        font-family:Arial;
        font-size:20px;
        font-weight:bold;

        box-shadow:0 0 15px rgba(0,234,255,0.5);

        white-space:nowrap;
    ">
        🌍 ANTARCTIC AI
        <span style="
            color:#7dff9b;
            font-size:11px;
            margin-left:12px;
        ">
            ● SYSTEM ONLINE
        </span>
    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(title_html)
    )

    # =========================================================
    # LEFT AI PANEL
    # =========================================================

    ai_panel = """
    <div style="
        position:fixed;
        top:75px;
        left:15px;
        z-index:5000;

        width:190px;

        background:rgba(5,15,25,0.95);
        color:white;

        padding:14px;

        border:1px solid #00eaff;
        border-radius:8px;

        font-family:Arial;
        font-size:12px;

        box-shadow:0 0 12px rgba(0,234,255,0.35);
    ">

        <div style="
            color:#00eaff;
            font-size:16px;
            font-weight:bold;
            margin-bottom:10px;
        ">
            🧠 AI STATUS
        </div>

        <div>🟢 System Online</div>
        <div>🟢 Vessel Tracking</div>
        <div>🟢 Ice Monitoring</div>
        <div>🟢 Navigation Active</div>

        <hr style="border-color:#29404a;">

        <div style="
            color:#00eaff;
            font-weight:bold;
        ">
            🚢 VESSELS
        </div>

        <div>Tracked: 06</div>
        <div>Our Ship: 01</div>
        <div>Other Ships: 05</div>

        <hr style="border-color:#29404a;">

        <div style="
            color:#00eaff;
            font-weight:bold;
        ">
            🧊 ICE DATA
        </div>

        <div>Detected: 03</div>
        <div>High Risk: 02</div>

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(ai_panel)
    )

    # =========================================================
    # LEGEND - BOTTOM LEFT
    # =========================================================

    legend_html = """
    <div style="
        position:fixed;
        bottom:55px;
        left:15px;
        z-index:5000;

        width:175px;

        background:rgba(5,15,25,0.96);
        color:white;

        padding:12px;

        border:1px solid #00eaff;
        border-radius:8px;

        font-family:Arial;
        font-size:12px;

        box-shadow:0 0 12px rgba(0,234,255,0.35);
    ">

        <div style="
            color:#00eaff;
            font-size:16px;
            font-weight:bold;
            margin-bottom:9px;
        ">
            🗺️ MAP LEGEND
        </div>

        <div style="margin:5px 0;">🚢 Our Research Ship</div>
        <div style="margin:5px 0;">🚢 Other Vessel</div>
        <div style="margin:5px 0;">🧊 Iceberg</div>
        <div style="margin:5px 0;">🟢 Low Ice</div>
        <div style="margin:5px 0;">🟡 Medium Ice</div>
        <div style="margin:5px 0;">🔴 Heavy Ice</div>
        <div style="margin:5px 0;">⚠️ AI Risk Area</div>
        <div style="margin:5px 0;">🛣️ AI Route</div>
        <div style="margin:5px 0;">🏁 Destination</div>

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(legend_html)
    )

    # =========================================================
    # COUNTRY BORDERS
    # =========================================================

    folium.GeoJson(
        "https://raw.githubusercontent.com/python-visualization/folium/main/examples/data/world-countries.json",
        name="🌍 Country Borders",

        style_function=lambda feature: {
            "fillColor": "transparent",
            "color": "#00eaff",
            "weight": 0.7,
            "fillOpacity": 0.03
        },

        tooltip=folium.GeoJsonTooltip(
            fields=["name"],
            aliases=["Country:"],
            labels=True
        )
    ).add_to(map_obj)

    # =========================================================
    # OUR SHIP
    # =========================================================

    ship_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:32px;
            text-align:center;
            filter:drop-shadow(0 0 8px #00eaff);
        ">
            🚢
        </div>
        """
    )

    folium.Marker(
        location=[-70, 20],

        tooltip="🚢 OUR RESEARCH SHIP",

        popup="""
        <div style="font-family:Arial;width:230px;">

            <h3>🚢 OUR RESEARCH SHIP</h3>

            <b>Latitude:</b> -70°<br>
            <b>Longitude:</b> 20°<br>
            <b>Speed:</b> 12.0 knots<br>
            <b>Heading:</b> 074°<br>
            <b>Destination:</b> Antarctic Research Station<br>
            <b>Status:</b> 🟢 ACTIVE<br>
            <b>AI Risk:</b> 🔴 HIGH

        </div>
        """,

        icon=ship_icon

    ).add_to(map_obj)

    # =========================================================
    # RADAR / MONITORING RANGE
    # =========================================================

    radar_center = [-70, 20]

    for radius in [150000, 300000, 450000]:

        folium.Circle(
            location=radar_center,
            radius=radius,
            color="#00eaff",
            weight=1,
            fill=False,
            tooltip="🛰️ AI Monitoring Range"
        ).add_to(map_obj)

    # =========================================================
    # OTHER VESSELS
    # =========================================================

    vessels = [

        ("Ocean Pioneer", 15, 20,
         "Research Vessel", "12.4 knots"),

        ("Polar Explorer", -35, 35,
         "Research Vessel", "10.8 knots"),

        ("Southern Star", -45, 70,
         "Cargo Vessel", "14.2 knots"),

        ("Atlantic Voyager", 10, -30,
         "Supply Vessel", "16.1 knots"),

        ("Ice Navigator", -55, 20,
         "Ice Research Vessel", "9.5 knots")
    ]

    vessel_icon = folium.DivIcon(
        html="""
        <div style="
            font-size:22px;
            text-align:center;
        ">
            🚢
        </div>
        """
    )

    for name, lat, lon, vessel_type, speed in vessels:

        folium.Marker(

            location=[lat, lon],

            tooltip=f"🚢 {name}",

            popup=f"""
            <b>🚢 {name}</b><br><br>

            <b>Type:</b> {vessel_type}<br>
            <b>Latitude:</b> {lat}°<br>
            <b>Longitude:</b> {lon}°<br>
            <b>Speed:</b> {speed}<br>
            <b>Status:</b> 🟢 ACTIVE

            """,

            icon=vessel_icon

        ).add_to(map_obj)

    # =========================================================
    # LOW ICE
    # =========================================================

    low_ice = [
        [-66, 5],
        [-65, 18],
        [-67, 28],
        [-69, 30],
        [-70, 18],
        [-69, 7]
    ]

    folium.Polygon(

        locations=low_ice,

        color="#00ff66",
        weight=2,

        fill=True,
        fill_color="#00ff66",
        fill_opacity=0.18,

        tooltip="🟢 LOW SEA ICE",
        popup="Low Sea-Ice Concentration"

    ).add_to(map_obj)

    # =========================================================
    # MEDIUM ICE
    # =========================================================

    medium_ice = [
        [-70, 5],
        [-69, 18],
        [-71, 32],
        [-74, 35],
        [-75, 25],
        [-74, 10]
    ]

    folium.Polygon(

        locations=medium_ice,

        color="#ffaa00",
        weight=2,

        fill=True,
        fill_color="#ffaa00",
        fill_opacity=0.22,

        tooltip="🟡 MEDIUM SEA ICE",
        popup="Medium Sea-Ice Concentration"

    ).add_to(map_obj)

    # =========================================================
    # HEAVY ICE
    # =========================================================

    heavy_ice = [
        [-74, 10],
        [-73, 25],
        [-75, 35],
        [-78, 30],
        [-79, 15],
        [-77, 5]
    ]

    folium.Polygon(

        locations=heavy_ice,

        color="#ff2222",
        weight=2,

        fill=True,
        fill_color="#ff2222",
        fill_opacity=0.25,

        tooltip="🔴 HEAVY SEA ICE",
        popup="Heavy Sea-Ice Concentration"

    ).add_to(map_obj)

    # =========================================================
    # AI RISK ZONE
    # =========================================================

    folium.Circle(

        location=[-72, 20],

        radius=500000,

        color="#ff0033",
        weight=2,

        fill=True,
        fill_color="#ff0033",
        fill_opacity=0.10,

        tooltip="⚠️ AI HIGH RISK AREA",
        popup="AI High Risk Zone"

    ).add_to(map_obj)

    # =========================================================
    # DESTINATION
    # =========================================================

    destination_icon = folium.DivIcon(

        html="""
        <div style="
            font-size:28px;
            text-align:center;
            filter:drop-shadow(0 0 8px #00ff66);
        ">
            🏁
        </div>
        """

    )

    folium.Marker(

        location=[-68, 30],

        tooltip="🏁 RESEARCH DESTINATION",

        popup="""
        <b>🏁 RESEARCH DESTINATION</b><br><br>

        Target: Antarctic Research Station<br>
        Navigation: ACTIVE

        """,

        icon=destination_icon

    ).add_to(map_obj)

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

        weight=5,

        opacity=0.9,

        dash_array="12,8",

        tooltip="🛰️ AI RECOMMENDED ROUTE"

    ).add_to(map_obj)

    # =========================================================
    # ICEBERG ICON
    # =========================================================

    iceberg_icon = folium.DivIcon(

        html="""
        <div style="
            font-size:25px;
            text-align:center;
            filter:drop-shadow(0 0 7px white);
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

        tooltip="🧊 ICEBERG 01 — HIGH RISK",

        popup="""
        <b>🧊 ICEBERG 01</b><br><br>

        Location: -71°, 25°<br>
        Size: Large<br>
        Movement: South-East<br>
        Risk: 🔴 HIGH

        """,

        icon=iceberg_icon

    ).add_to(map_obj)

    folium.PolyLine(

        locations=[
            [-71, 25],
            [-70.5, 26],
            [-70, 27]
        ],

        color="#ff2222",
        weight=3,

        tooltip="Iceberg 01 Movement"

    ).add_to(map_obj)

    # =========================================================
    # ICEBERG 02
    # =========================================================

    folium.Marker(

        location=[-73, 15],

        tooltip="🧊 ICEBERG 02 — MEDIUM RISK",

        popup="""
        <b>🧊 ICEBERG 02</b><br><br>

        Location: -73°, 15°<br>
        Size: Medium<br>
        Movement: East<br>
        Risk: 🟡 MEDIUM

        """,

        icon=iceberg_icon

    ).add_to(map_obj)

    folium.PolyLine(

        locations=[
            [-73, 15],
            [-73, 17],
            [-73, 19]
        ],

        color="#ffaa00",
        weight=3,

        tooltip="Iceberg 02 Movement"

    ).add_to(map_obj)

    # =========================================================
    # ICEBERG 03
    # =========================================================

    folium.Marker(

        location=[-75, 28],

        tooltip="🧊 ICEBERG 03 — HIGH RISK",

        popup="""
        <b>🧊 ICEBERG 03</b><br><br>

        Location: -75°, 28°<br>
        Size: Large<br>
        Movement: South<br>
        Risk: 🔴 HIGH

        """,

        icon=iceberg_icon

    ).add_to(map_obj)

    folium.PolyLine(

        locations=[
            [-75, 28],
            [-76, 28],
            [-77, 28]
        ],

        color="#ff2222",
        weight=3,

        tooltip="Iceberg 03 Movement"

    ).add_to(map_obj)

    # =========================================================
    # LAYER CONTROL
    # =========================================================

    folium.LayerControl(
        position="bottomright",
        collapsed=False
    ).add_to(map_obj)

    # =========================================================
    # BOTTOM STATUS BAR
    # =========================================================

    status_bar = """
    <div style="
        position:fixed;
        bottom:10px;
        left:50%;
        transform:translateX(-50%);
        z-index:5000;

        background:rgba(5,15,25,0.96);

        color:#00eaff;

        padding:8px 18px;

        border:1px solid #00eaff;
        border-radius:6px;

        font-family:Arial;
        font-size:12px;

        box-shadow:0 0 10px rgba(0,234,255,0.4);

        white-space:nowrap;
    ">

        🌍 GLOBAL
        &nbsp;|&nbsp;
        🚢 VESSELS
        &nbsp;|&nbsp;
        🧊 ICE
        &nbsp;|&nbsp;
        🧠 AI
        &nbsp;|&nbsp;
        🛰️ NAVIGATION

    </div>
    """

    map_obj.get_root().html.add_child(
        folium.Element(status_bar)
    )

    # =========================================================
    # WORLD VIEW
    # =========================================================

    map_obj.fit_bounds(
        [
            [-60, -170],
            [80, 170]
        ]
    )

    # =========================================================
    # RETURN MAP
    # =========================================================

    return map_obj