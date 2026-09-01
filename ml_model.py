import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error


DATA_FILE = "ml_data/antarctic_prototype_data.csv"


def load_data():
    return pd.read_csv(DATA_FILE)


def train_sea_ice_model():

    data = load_data()

    data["day_number"] = range(1, len(data) + 1)

    X = data[["day_number"]]
    y = data["sea_ice_concentration"]

    model = LinearRegression()

    model.fit(X, y)

    predictions = model.predict(X)

    mae = mean_absolute_error(y, predictions)

    return model, mae


def predict_sea_ice(model, day_number):

    input_data = pd.DataFrame({
        "day_number": [day_number]
    })

    prediction = model.predict(input_data)[0]

    prediction = max(0, min(100, prediction))

    return round(float(prediction), 2)


def get_sea_ice_prediction(days_ahead=3):

    if not isinstance(days_ahead, int):
        raise ValueError("days_ahead must be an integer")

    if days_ahead < 1:
        raise ValueError("days_ahead must be at least 1")

    if days_ahead > 30:
        raise ValueError("days_ahead cannot exceed 30")

    model, mae = train_sea_ice_model()

    data = load_data()

    last_day = len(data)

    predictions = []

    for day in range(1, days_ahead + 1):

        future_day = last_day + day

        prediction = predict_sea_ice(
            model,
            future_day
        )

        predictions.append({
            "day_ahead": day,
            "predicted_sea_ice_concentration": prediction
        })

    return {
        "status": "success",
        "prediction_status": "prototype",
        "model_type": "Linear Regression",
        "data_source": DATA_FILE,
        "is_ml_trained": True,
        "mae": round(float(mae), 2),
        "forecast_days": days_ahead,
        "predictions": predictions
    }


if __name__ == "__main__":

    result = get_sea_ice_prediction(3)

    print("=== ML SEA-ICE MODEL ===")
    print("Status:", result["status"])
    print("Prediction Status:", result["prediction_status"])
    print("Model Type:", result["model_type"])
    print("Data Source:", result["data_source"])
    print("ML Trained:", result["is_ml_trained"])
    print("MAE:", result["mae"])
    print("Forecast Days:", result["forecast_days"])

    print("\n=== FUTURE PREDICTIONS ===")

    for prediction in result["predictions"]:

        print(
            f"Day {prediction['day_ahead']}: "
            f"{prediction['predicted_sea_ice_concentration']}%"
        )