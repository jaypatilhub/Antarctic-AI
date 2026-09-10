from ml_model import get_sea_ice_prediction
from ml_prediction import predict_iceberg_trajectory, load_data


def get_ai_predictions(days_ahead=3):

    if not isinstance(days_ahead, int):
        raise ValueError("days_ahead must be an integer")

    if days_ahead < 1:
        raise ValueError("days_ahead must be at least 1")

    if days_ahead > 30:
        raise ValueError("days_ahead cannot exceed 30")

    # ==============================
    # SEA-ICE PREDICTION
    # ==============================

    sea_ice_result = get_sea_ice_prediction(days_ahead)

    sea_ice_predictions = []

    for prediction in sea_ice_result["predictions"]:
        sea_ice_predictions.append({
            "day_ahead": int(prediction["day_ahead"]),
            "predicted_sea_ice_concentration": float(
                prediction["predicted_sea_ice_concentration"]
            )
        })

    # ==============================
    # ICEBERG TRAJECTORY PREDICTION
    # ==============================

    data = load_data()

    iceberg_predictions_raw = predict_iceberg_trajectory(
        data,
        days_ahead
    )

    iceberg_predictions = []

    for prediction in iceberg_predictions_raw:
        iceberg_predictions.append({
            "day_ahead": int(prediction["day_ahead"]),
            "predicted_latitude": float(
                prediction["predicted_latitude"]
            ),
            "predicted_longitude": float(
                prediction["predicted_longitude"]
            ),
            "speed_kmh": float(
                prediction["speed_kmh"]
            ),
            "direction": str(
                prediction["direction"]
            )
        })

    # ==============================
    # FINAL AI OUTPUT
    # ==============================

    return {
        "status": "success",
        "prediction_status": "prototype",
        "model_type": "Linear Regression + prototype iceberg trajectory",
        "data_source": "ml_data/antarctic_prototype_data.csv",
        "is_ml_trained": True,
        "sea_ice_mae": float(
            sea_ice_result["mae"]
        ),
        "forecast_days": int(days_ahead),
        "sea_ice_prediction": sea_ice_predictions,
        "iceberg_prediction": iceberg_predictions
    }


# ==============================
# TEST
# ==============================

if __name__ == "__main__":

    result = get_ai_predictions(days_ahead=3)

    print("\n=== AI PREDICTION MODULE ===")
    print("Status:", result["status"])
    print("Model:", result["model_type"])
    print("ML Trained:", result["is_ml_trained"])
    print("Sea-Ice MAE:", result["sea_ice_mae"])

    print("\n=== SEA-ICE PREDICTION ===")

    for prediction in result["sea_ice_prediction"]:
        print(prediction)

    print("\n=== ICEBERG TRAJECTORY ===")

    for prediction in result["iceberg_prediction"]:
        print(prediction)
