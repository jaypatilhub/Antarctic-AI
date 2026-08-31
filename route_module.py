def calculate_route_risk(distance_km, ice_risk):
    """
    Calculates a prototype route risk level.

    This is a rule-based prototype, not a real
    scientific navigation model.
    """

    ice_risk = ice_risk.strip().upper()

    if distance_km < 0:
        return "INVALID"

    if ice_risk not in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]:
        return "INVALID"

    if distance_km < 5 or ice_risk == "HIGH":
        return "DANGER"

    elif distance_km < 15 or ice_risk == "MEDIUM":
        return "CAUTION"

    else:
        return "SAFE"
def calculate_fuel(distance_km, fuel_per_km, fuel_cost_per_liter):
    """
    Estimates fuel usage and fuel cost for a route.

    This is a simple prototype estimate,
    not a real scientific vessel fuel model.
    """

    if distance_km < 0 or fuel_per_km <= 0 or fuel_cost_per_liter < 0:
        return {
            "status": "INVALID",
            "estimated_fuel_liters": 0,
            "estimated_fuel_cost": 0
        }

    estimated_fuel = distance_km * fuel_per_km
    estimated_cost = estimated_fuel * fuel_cost_per_liter

    return {
        "status": "VALID",
        "estimated_fuel_liters": round(estimated_fuel, 2),
        "estimated_fuel_cost": round(estimated_cost, 2)
    }
def compare_safety_fuel(route_a, route_b, fuel_per_km, fuel_cost_per_liter):
    """
    Compares two routes using safety first and fuel second.

    This is a simple prototype comparison, not a real
    scientific navigation optimization model.
    """

    risk_order = {
        "SAFE": 1,
        "CAUTION": 2,
        "DANGER": 3,
        "INVALID": 4
    }

    risk_a = calculate_route_risk(
        route_a["distance_km"],
        route_a["ice_risk"]
    )

    risk_b = calculate_route_risk(
        route_b["distance_km"],
        route_b["ice_risk"]
    )

    fuel_a = calculate_fuel(
        route_a["distance_km"],
        fuel_per_km,
        fuel_cost_per_liter
    )

    fuel_b = calculate_fuel(
        route_b["distance_km"],
        fuel_per_km,
        fuel_cost_per_liter
    )

    if risk_order[risk_a] < risk_order[risk_b]:
        recommended = "Route A"

    elif risk_order[risk_b] < risk_order[risk_a]:
        recommended = "Route B"

    elif fuel_a["estimated_fuel_liters"] <= fuel_b["estimated_fuel_liters"]:
        recommended = "Route A"

    else:
        recommended = "Route B"

    return {
        "route_a_risk": risk_a,
        "route_b_risk": risk_b,
        "route_a_fuel_liters": fuel_a["estimated_fuel_liters"],
        "route_b_fuel_liters": fuel_b["estimated_fuel_liters"],
        "route_a_fuel_cost": fuel_a["estimated_fuel_cost"],
        "route_b_fuel_cost": fuel_b["estimated_fuel_cost"],
        "recommended_route": recommended
    }
def recommend_route(distance_km, ice_risk):
    """
    Returns a route recommendation based on route risk.
    """

    risk = calculate_route_risk(distance_km, ice_risk)

    if risk == "INVALID":
        return {
            "status": "INVALID",
            "recommendation": "Invalid route input provided.",
            "reason": "Invalid distance or ice risk."
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
    Compares two candidate routes and recommends a safer route.
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

def rank_routes(routes, fuel_per_km, fuel_cost_per_liter):
    """
    Ranks candidate routes using safety first and fuel second.

    This is a simple prototype ranking system,
    not a real scientific navigation algorithm.
    """

    risk_order = {
        "SAFE": 1,
        "CAUTION": 2,
        "DANGER": 3,
        "INVALID": 4
    }

    ranked_routes = []

    for route in routes:
        risk = calculate_route_risk(
            route["distance_km"],
            route["ice_risk"]
        )

        fuel = calculate_fuel(
            route["distance_km"],
            fuel_per_km,
            fuel_cost_per_liter
        )

        ranked_routes.append({
            "name": route.get("name", "Unnamed Route"),
            "distance_km": route["distance_km"],
            "risk": risk,
            "fuel_liters": fuel["estimated_fuel_liters"],
            "fuel_cost": fuel["estimated_fuel_cost"]
        })

    ranked_routes.sort(
        key=lambda route: (
            risk_order[route["risk"]],
            route["fuel_liters"]
        )
    )

    return ranked_routes
def replan_route(current_route, alternative_routes):
    """
    Re-plans the route when the current route becomes unsafe.

    Safety priority:
    SAFE > CAUTION > DANGER

    This is a prototype rule-based route re-planning function,
    not a real-time scientific navigation system.
    """

    risk_order = {
        "SAFE": 1,
        "CAUTION": 2,
        "DANGER": 3,
        "INVALID": 4
    }

    current_risk = calculate_route_risk(
        current_route["distance_km"],
        current_route["ice_risk"]
    )

    if current_risk == "SAFE":
        return {
            "status": "SAFE",
            "recommendation": "Current route is safe. No re-planning required.",
            "route": current_route
        }

    if not alternative_routes:
        return {
            "status": "DANGER",
            "recommendation": "No alternative route available.",
            "route": None
        }

    evaluated_routes = []

    for route in alternative_routes:
        risk = calculate_route_risk(
            route["distance_km"],
            route["ice_risk"]
        )

        evaluated_routes.append({
            **route,
            "calculated_risk": risk
        })

    safer_routes = [
        route
        for route in evaluated_routes
        if risk_order[route["calculated_risk"]] < risk_order[current_risk]
    ]

    if not safer_routes:
        return {
            "status": "DANGER",
            "recommendation": "No safer alternative route found.",
            "route": None
        }

    new_route = min(
        safer_routes,
        key=lambda route: (
            risk_order[route["calculated_risk"]],
            route["distance_km"]
        )
    )

    return {
        "status": "REPLANNED",
        "recommendation": "Current route replaced with a safer alternative.",
        "route": new_route
    }
def recommend_best_route(routes):
    """
    Selects the safest route from multiple candidate routes.

    This is a prototype rule-based selection,
    not a real scientific navigation algorithm.
    """

    if not routes:
        return {
            "status": "INVALID",
            "recommendation": "No candidate routes provided."
        }

    safe_routes = []

    for route in routes:
        risk = calculate_route_risk(
            route["distance_km"],
            route["ice_risk"]
        )

        if risk == "SAFE":
            safe_routes.append(route)

    if not safe_routes:
        return {
            "status": "DANGER",
            "recommendation": "No safe candidate route found."
        }

    best_route = min(
        safe_routes,
        key=lambda route: route["distance_km"]
    )

    return {
        "status": "SAFE",
        "recommendation": "Safest candidate route selected.",
        "route": best_route
    }


if __name__ == "__main__":
    test_cases = [
        (3, "HIGH"),
        (10, "MEDIUM"),
        (20, "LOW"),
        (50, "LOW")
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
    Select the safest route first.
    Fuel cost is considered only when routes have the same risk level.
    """

    if not routes:
        raise ValueError("At least one route is required.")

    risk_priority = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    ranked_routes = []

    for route in routes:
        risk_level = route["risk_level"].strip().upper()

        if risk_level not in risk_priority:
            raise ValueError(
                "Risk level must be LOW, MEDIUM, HIGH, or CRITICAL."
            )

        score = calculate_route_score(
            route["distance_km"],
            route["fuel_cost"],
            risk_level
        )

        ranked_routes.append({
            "name": route["name"],
            "distance_km": route["distance_km"],
            "fuel_cost": route["fuel_cost"],
            "risk_level": risk_level,
            "score": score
        })

    ranked_routes.sort(
        key=lambda route: (
            risk_priority[route["risk_level"]],
            route["fuel_cost"]
        )
    )

    safe_routes = [
        route for route in ranked_routes
        if route["risk_level"] == "LOW"
    ]

    if not safe_routes:
        return {
            "recommended_route": None,
            "all_routes": ranked_routes,
            "status": "NO_SAFE_ROUTE",
            "message": "No safe route available. Search for an alternative route."
        }

    return {
        "recommended_route": safe_routes[0],
        "all_routes": ranked_routes,
        "status": "SAFE_ROUTE_FOUND",
        "message": "Safest available route selected.",
        "reason": f"Route {safe_routes[0]['name']} selected because it has the lowest risk level ({safe_routes[0]['risk_level']})."
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
 return recommend_best_route(routes)