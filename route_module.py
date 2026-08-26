def calculate_route_risk(distance_km, ice_risk):
    """
    Simple demo logic for Antarctic safe-route assessment.
    This is a prototype rule-based system, not a real navigation model.
    """

    if distance_km < 5 or ice_risk == "HIGH":
        return "DANGER"

    elif distance_km < 15 or ice_risk == "MEDIUM":
        return "CAUTION"

    else:
        return "SAFE"


def recommend_route(distance_km, ice_risk):
    """
    Returns a simple route recommendation.
    """

    risk = calculate_route_risk(distance_km, ice_risk)

    if risk == "DANGER":
        return {
            "status": "DANGER",
            "recommendation": "Avoid this route and search for an alternative route."
        }

    elif risk == "CAUTION":
        return {
            "status": "CAUTION",
            "recommendation": "Proceed carefully and monitor ice conditions."
        }

    else:
        return {
            "status": "SAFE",
            "recommendation": "Route appears suitable for the prototype conditions."
        }


if __name__ == "__main__":
    test_cases = [
        (3, "HIGH"),
        (10, "MEDIUM"),
        (20, "LOW"),
        (50, "LOW"),
    ]

    for distance, ice_risk in test_cases:
        result = recommend_route(distance, ice_risk)

        print(
            f"Distance: {distance} km | "
            f"Ice Risk: {ice_risk} | "
            f"Status: {result['status']} | "
            f"Recommendation: {result['recommendation']}"
        )