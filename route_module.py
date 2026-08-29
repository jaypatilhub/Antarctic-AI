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
        
def calculate_route_score(distance_km, fuel_cost, risk_level):
    """
    Calculate a simple explainable route score.

    Lower score = better route.
    Distance and fuel increase the score.
    Higher risk adds a larger penalty.
    """

    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    if fuel_cost < 0:
        raise ValueError("Fuel cost cannot be negative.")

    risk_level = risk_level.strip().upper()

    risk_penalty = {
        "LOW": 0,
        "MEDIUM": 20,
        "HIGH": 50,
        "CRITICAL": 100
    }

    if risk_level not in risk_penalty:
        raise ValueError(
            "Risk level must be LOW, MEDIUM, HIGH, or CRITICAL."
        )

    return distance_km + fuel_cost + risk_penalty[risk_level]

def rank_routes(routes):
    """
    Rank candidate routes from best to worst.

    Lower route score = better route.
    """

    if not routes:
        raise ValueError("At least one route is required.")

    ranked_routes = []

    for route in routes:
        score = calculate_route_score(
            route["distance_km"],
            route["fuel_cost"],
            route["risk_level"]
        )

        ranked_routes.append({
            "name": route["name"],
            "distance_km": route["distance_km"],
            "fuel_cost": route["fuel_cost"],
            "risk_level": route["risk_level"],
            "score": score
        })

    ranked_routes.sort(key=lambda route: route["score"])

    return ranked_routes

def recommend_best_route(routes):
    """
    Select the highest-ranked candidate route.

    The first route after ranking is the recommended route.
    """

    ranked_routes = rank_routes(routes)

    return {
        "recommended_route": ranked_routes[0],
        "all_routes": ranked_routes
    }
    
def compare_safety_and_fuel(route):
    """
    Explain the trade-off between route safety and fuel usage.
    """

    risk_level = route["risk_level"].strip().upper()
    fuel_cost = route["fuel_cost"]

    if risk_level in ["HIGH", "CRITICAL"]:
        safety_priority = "HIGH"
    elif risk_level == "MEDIUM":
        safety_priority = "MEDIUM"
    else:
        safety_priority = "LOW"

    if fuel_cost <= 20:
        fuel_priority = "FUEL-EFFICIENT"
    else:
        fuel_priority = "FUEL-COSTLY"

    return {
        "route": route["name"],
        "safety_priority": safety_priority,
        "fuel_priority": fuel_priority
    }
    
def replan_routes(routes):
    """
    Re-rank routes when risk or fuel conditions change.
    """

    return recommend_best_route(routes)