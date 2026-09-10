from ml_prediction import run_predictions

result = run_predictions(days_ahead=3)

clean_result = {
    "status": "success",
    "forecast_days": 3,
    "sea_ice_prediction": [
        {
            "day_ahead": int(p["day_ahead"]),
            "predicted_sea_ice_concentration": float(
                p["predicted_sea_ice_concentration"]
            )
        }
        for p in result["sea_ice_prediction"]
    ],
    "iceberg_prediction": [
        {
            "day_ahead": int(p["day_ahead"]),
            "predicted_latitude": float(p["predicted_latitude"]),
            "predicted_longitude": float(p["predicted_longitude"]),
            "speed_kmh": float(p["speed_kmh"]),
            "direction": str(p["direction"])
        }
        for p in result["iceberg_prediction"]
    ]
}

print(clean_result)
