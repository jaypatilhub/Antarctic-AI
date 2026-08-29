def calculate_risk(distance_km):
    """
    Calculate iceberg collision risk based on distance.
    """
    
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")
    
    if distance_km <= 5:
        return "CRITICAL"

    elif distance_km <= 15:
        return "HIGH"

    elif distance_km <= 30:
        return "MEDIUM"

    else:
        return "LOW"
    
def classify_sea_ice_concentration(concentration):
    """
    Convert sea-ice concentration percentage into a condition.
    Prototype rule-based classification.
    """

    if concentration < 0 or concentration > 100:
        raise ValueError("Sea-ice concentration must be between 0 and 100.")

    if concentration >= 80:
        return "HEAVY"

    elif concentration >= 50:
        return "MODERATE"

    else:
        return "LIGHT"


def assess_sea_ice(sea_ice_condition):
    """
    Assess sea-ice condition for the prototype.
    This is demo/rule-based logic, not a scientific prediction.
    """

    if sea_ice_condition == "HEAVY":
        return "HIGH"

    elif sea_ice_condition == "MODERATE":
        return "MEDIUM"

    elif sea_ice_condition == "LIGHT":
        return "LOW"

    else:
        raise ValueError(
            "Sea-ice condition must be LIGHT, MODERATE, or HEAVY."
        )


def calculate_overall_risk(distance, sea_ice_condition):
    """
    Calculate overall risk using distance and sea-ice condition.
    """

    distance_risk = calculate_risk(distance)
    ice_risk = assess_sea_ice(sea_ice_condition)

    risk_levels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    if risk_levels[distance_risk] >= risk_levels[ice_risk]:
        return distance_risk
    else:
        return ice_risk
    
def calculate_risk_from_data(distance_km, sea_ice_concentration):
    """
    Calculate overall risk using distance and sea-ice concentration.
    """

    sea_ice_condition = classify_sea_ice_concentration(
        sea_ice_concentration
    )

    return calculate_overall_risk(
        distance_km,
        sea_ice_condition
    )
    
def assess_trajectory_risk(speed_knots=None, heading_degrees=None):
    """
    Prepare trajectory-related inputs for future risk analysis.

    This prototype does not calculate trajectory risk yet.
    It only validates the trajectory inputs so a future
    risk model can use them safely.
    """

    if speed_knots is not None and speed_knots < 0:
        raise ValueError("Speed cannot be negative.")

    if heading_degrees is not None and not 0 <= heading_degrees <= 360:
        raise ValueError("Heading must be between 0 and 360 degrees.")

    return {
        "speed_knots": speed_knots,
        "heading_degrees": heading_degrees,
        "trajectory_risk": None
    }
    
def get_risk_explanation(distance_km, sea_ice_concentration):
    """
    Provide a clear explanation for the overall risk.
    Prototype rule-based explanation.
    """

    overall_risk = calculate_risk_from_data(
        distance_km,
        sea_ice_concentration
    )

    distance_risk = calculate_risk(distance_km)

    sea_ice_condition = classify_sea_ice_concentration(
        sea_ice_concentration
    )

    return (
        f"Risk: {overall_risk}. "
        f"Iceberg distance risk: {distance_risk}. "
        f"Sea-ice condition: {sea_ice_condition} "
        f"({sea_ice_concentration}%)."
    )
            
    
def get_risk_reason(distance_km):
    """
    Give a clear explanation for the calculated risk.
    """

    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    if distance_km <= 5:
        return "CRITICAL: Vessel is extremely close to an iceberg."

    elif distance_km <= 15:
        return "HIGH: Vessel is relatively close to an iceberg."

    elif distance_km <= 30:
        return "MEDIUM: Vessel has a moderate distance from an iceberg."

    else:
        return "LOW: Vessel is at a relatively safe distance from an iceberg."

if __name__ == "__main__":
    test_distances = [3, 10, 20, 50]

    for distance in test_distances:
        risk = calculate_risk(distance)
        reason = get_risk_reason(distance)

        print(f"Distance: {distance} km → Risk: {risk}")
        print(f"Reason: {reason}")
        print()