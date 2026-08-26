def calculate_risk(distance_km):
    """
    Calculate iceberg collision risk based on distance.
    """

    if distance_km <= 5:
        return "CRITICAL"

    elif distance_km <= 15:
        return "HIGH"

    elif distance_km <= 30:
        return "MEDIUM"

    else:
        return "LOW"


if __name__ == "__main__":
    test_distances = [3, 10, 20, 50]

    for distance in test_distances:
        risk = calculate_risk(distance)
        print(f"Distance: {distance} km → Risk: {risk}")