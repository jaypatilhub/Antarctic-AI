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


def validate_data(df):
    required_columns = [
        "latitude",
        "longitude",
        "iceberg_id",
        "sea_ice_concentration"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing required column: {column}")

    if df["latitude"].isnull().any():
        raise ValueError("Latitude contains missing values")

    if df["longitude"].isnull().any():
        raise ValueError("Longitude contains missing values")

    if df["sea_ice_concentration"].isnull().any():
        raise ValueError("Sea ice concentration contains missing values")

    if not df["latitude"].between(-90, 90).all():
        raise ValueError("Invalid latitude value")

    if not df["longitude"].between(-180, 180).all():
        raise ValueError("Invalid longitude value")

    if not df["sea_ice_concentration"].between(0, 100).all():
        raise ValueError("Invalid sea ice concentration")

    return True
def clean_data(df):
    df = df.copy()

    df = df.drop_duplicates()

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["sea_ice_concentration"] = pd.to_numeric(
        df["sea_ice_concentration"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "latitude",
            "longitude",
            "iceberg_id",
            "sea_ice_concentration"
        ]
    )

    df = df.reset_index(drop=True)

    return df
def preprocess_data(df):
    df = df.copy()

    df["latitude"] = df["latitude"].astype(float)
    df["longitude"] = df["longitude"].astype(float)
    df["sea_ice_concentration"] = df["sea_ice_concentration"].astype(float)

    df["iceberg_id"] = df["iceberg_id"].astype(str)

    return df