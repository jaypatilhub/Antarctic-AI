import pandas as pd
import folium


def load_map_data(file_path):
    """
    Load processed Antarctic sea-ice CSV data
    for map visualization.
    """

    df = pd.read_csv(file_path)

    required_columns = [
        "latitude",
        "longitude",
        "sea_ice_concentration"
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    return df


def create_map(df):
    """
    Create an Antarctic map using latitude and longitude data.
    """

    m = folium.Map(
        location=[-75, 0],
        zoom_start=3
    )

    return m


if __name__ == "__main__":

    input_file = "./data/processed/20250101_sea_ice.csv"

    df = load_map_data(input_file)

    print("Map data loaded successfully")
    print("Rows:", len(df))
    print("Columns:", df.columns.tolist())

    m = create_map(df)

    print("Map created successfully")