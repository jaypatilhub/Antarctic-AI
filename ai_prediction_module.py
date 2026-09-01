from ml_prediction import run_predictions


def get_ai_predictions(days_ahead=3):

    if not isinstance(days_ahead, int):
        raise ValueError("days_ahead must be an integer")

    if days_ahead < 1:
        raise ValueError("days_ahead must be at least 1")

    if days_ahead > 30:
        raise ValueError("days_ahead cannot exceed 30")

    result = run_predictions(days_ahead=days_ahead)

    sea_ice_predictions = []

    for prediction in result["sea_ice_prediction"]:
        sea_ice_predictions.append({
            "day_ahead": int(prediction["day_ahead"]),
            "predicted_sea_ice_concentration": float(
                prediction["predicted_sea_ice_concentration"]
            )
        })

    iceberg_predictions = []

    for prediction in result["iceberg_prediction"]:
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

    return {
        "status": "success",
        "prediction_status": "prototype",
        "model_type": "trend_based_prototype",
        "data_source": "ml_data/antarctic_prototype_data.csv",
        "is_ml_trained": False,
        "forecast_days": int(days_ahead),
        "sea_ice_prediction": sea_ice_predictions,
        "iceberg_prediction": iceberg_predictions
    }


if __name__ == "__main__":

    predictions = get_ai_predictions(days_ahead=3)

    print("=== AI PREDICTION MODULE ===")
    print("Status:", predictions["status"])
    print("Prediction Status:", predictions["prediction_status"])
    print("Model Type:", predictions["model_type"])
    print("Data Source:", predictions["data_source"])
    print("ML Trained:", predictions["is_ml_trained"])
    print("Forecast Days:", predictions["forecast_days"])

    print("\n=== SEA-ICE PREDICTION ===")

    for prediction in predictions["sea_ice_prediction"]:
        print(prediction)

    print("\n=== ICEBERG TRAJECTORY ===")

    for prediction in predictions["iceberg_prediction"]:
        print(prediction)
