def calculate_route_risk(distance_km, ice_risk):
    """
    Simple demo logic for Antarctic safe-route assessment.
    This is a prototype rule-based system, not a real navigation model.
    """

    ice_risk = ice_risk.strip().upper()

    if distance_km < 0:
        return "INVALID"

    if ice_risk not in ["LOW", "MEDIUM", "HIGH"]:
        return "INVALID"

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

    if risk == "INVALID":
        return {
            "status": "INVALID",
            "recommendation": "Invalid route input provided."
        }

    elif risk == "DANGER":
        return {
            "status": "DANGER",
            "recommendation": "Avoid this route and search for an alternative route.",
            "reason": "High ice risk or very short route distance."
        }

    elif risk == "CAUTION":
        return {
            "status": "CAUTION",
            "recommendation": "Proceed carefully and monitor ice conditions.",
            "reason": "Medium risk condition detected."
        }

    else:
        return {
            "status": "SAFE",
            "recommendation": "Route appears suitable for the prototype conditions.",
            "reason": "Low risk condition detected."
        }


def compare_routes(route_a, route_b):
    """
    Compares two demo routes and returns their risk levels.
    """

    risk_a = calculate_route_risk(
        route_a["distance_km"],
        route_a["ice_risk"]
    )

    risk_b = calculate_route_risk(
        route_b["distance_km"],
        route_b["ice_risk"]
    )

    if risk_a == "SAFE" and risk_b != "SAFE":
            recommended = "Route A"

    elif risk_b == "SAFE" and risk_a != "SAFE":
        recommended = "Route B"

    elif risk_a == "SAFE" and risk_b == "SAFE":
        recommended = "Route A"

    else:
        recommended = "No safe route"

    return {
        "route_a_risk": risk_a,
        "route_b_risk": risk_b,
        "recommended_route": recommended
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
            f"Recommendation: {result['recommendation']} | "
            f"Reason: {result['reason']}"
        )