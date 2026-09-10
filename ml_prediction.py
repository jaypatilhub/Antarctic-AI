import pandas as pd

DATA_FILE = "ml_data/antarctic_prototype_data.csv"


def load_data():
    """Load the Antarctic prototype dataset."""
    return pd.read_csv(DATA_FILE)


def predict_sea_ice(data, days_ahead=3):
    """
    Prototype sea-ice prediction.
    Uses recent observations to estimate future
    sea-ice concentration.
    """
    recent = data["sea_ice_concentration"].tail(5)

    daily_change = recent.diff().mean()
    current_value = recent.iloc[-1]

    predictions = []

    for day in range(1, days_ahead + 1):
        predicted_value = current_value + (daily_change * day)

        # Keep sea-ice concentration between 0% and 100%
        predicted_value = max(0, min(100, predicted_value))

        predictions.append({
            "day_ahead": day,
            "predicted_sea_ice_concentration": round(
                predicted_value, 2
            )
        })

    return predictions


def predict_iceberg_trajectory(data, days_ahead=3):
    """
    Prototype iceberg trajectory prediction.

    Uses the latest iceberg position, speed and direction
    to estimate future positions.
    """

    latest = data.iloc[-1]

    latitude = float(latest["iceberg_latitude"])
    longitude = float(latest["iceberg_longitude"])
    speed = float(latest["iceberg_speed_kmh"])
    direction = str(latest["iceberg_direction"])

    predictions = []

    for day in range(1, days_ahead + 1):

        # Prototype movement for SE direction
        latitude_change = -0.15 * day
        longitude_change = 0.15 * day

        predicted_latitude = latitude + latitude_change
        predicted_longitude = longitude + longitude_change

        predictions.append({
            "day_ahead": day,
            "predicted_latitude": round(
                predicted_latitude, 3
            ),
            "predicted_longitude": round(
                predicted_longitude, 3
            ),
            "speed_kmh": speed,
            "direction": direction
        })

    return predictions


def run_predictions(days_ahead=3):
    """Run both sea-ice and iceberg predictions."""

    if not isinstance(days_ahead, int):
        raise ValueError("days_ahead must be an integer")

    if days_ahead < 1:
        raise ValueError("days_ahead must be at least 1")

    if days_ahead > 30:
        raise ValueError("days_ahead cannot exceed 30")

    data = load_data()

    sea_ice_prediction = predict_sea_ice(
        data,
        days_ahead
    )

    iceberg_prediction = predict_iceberg_trajectory(
        data,
        days_ahead
    )

    return {
        "sea_ice_prediction": sea_ice_prediction,
        "iceberg_prediction": iceberg_prediction
    }


if __name__ == "__main__":

    results = run_predictions(days_ahead=3)

    print("\n=== SEA-ICE PREDICTION ===")

    for prediction in results["sea_ice_prediction"]:
        print(prediction)

    print("\n=== ICEBERG TRAJECTORY PREDICTION ===")

    for prediction in results["iceberg_prediction"]:
        print(prediction)