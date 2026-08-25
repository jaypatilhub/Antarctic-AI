import pandas as pd


def load_data():
    data = {
        "latitude": [-70.5, -71.2],
        "longitude": [20.3, 21.8],
        "iceberg_id": ["IB001", "IB002"],
        "sea_ice_concentration": [85, 72]
    }

    df = pd.DataFrame(data)

    return df