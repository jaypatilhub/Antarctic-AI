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


def calculate_ice_and_sea_ice_risk(distance, sea_ice_condition):
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

    return calculate_ice_and_sea_ice_risk(
        distance_km,
        sea_ice_condition
    )
            
        
def get_risk_reason(distance_km):
    """
    Give a simple explanation for the calculated risk.
    """

    if distance_km <= 5:
        return "Vessel is extremely close to an iceberg."

    elif distance_km <= 15:
        return "Vessel is relatively close to an iceberg."

    elif distance_km <= 30:
        return "Vessel has a moderate distance from an iceberg."

    else:
        return "Vessel is at a relatively safe distance from an iceberg."


if __name__ == "__main__":
    test_distances = [3, 10, 20, 50]

    for distance in test_distances:
        risk = calculate_risk(distance)
        reason = get_risk_reason(distance)

        print(f"Distance: {distance} km → Risk: {risk}")
        print(f"Reason: {reason}")
        print()
# M4 Risk & Safety Upgrade - Demo/Simulation Logic


def calculate_ice_risk(iceberg_distance_km, sea_ice_concentration):
    """
    Calculate ice-related navigation risk.
    Demo/simulation rule-based logic only.
    """

    if iceberg_distance_km < 0:
        raise ValueError("Iceberg distance cannot be negative.")

    if sea_ice_concentration < 0 or sea_ice_concentration > 100:
        raise ValueError(
            "Sea-ice concentration must be between 0 and 100."
        )

    iceberg_risk = calculate_risk(iceberg_distance_km)
    sea_ice_condition = classify_sea_ice_concentration(
        sea_ice_concentration
    )
    sea_ice_risk = assess_sea_ice(sea_ice_condition)

    risk_levels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    if risk_levels[iceberg_risk] >= risk_levels[sea_ice_risk]:
        return iceberg_risk
    else:
        return sea_ice_risk


def calculate_weather_risk(wind_speed_knots, wave_height_m):
    """
    Calculate weather-related navigation risk.
    Demo/simulation rule-based logic only.
    """

    if wind_speed_knots < 0:
        raise ValueError("Wind speed cannot be negative.")

    if wave_height_m < 0:
        raise ValueError("Wave height cannot be negative.")

    if wind_speed_knots >= 40 or wave_height_m >= 6:
        return "CRITICAL"

    elif wind_speed_knots >= 30 or wave_height_m >= 4:
        return "HIGH"

    elif wind_speed_knots >= 20 or wave_height_m >= 2:
        return "MEDIUM"

    else:
        return "LOW"


def calculate_ocean_risk(current_speed_knots, wave_height_m):
    """
    Calculate ocean-related navigation risk.
    Demo/simulation rule-based logic only.
    """

    if current_speed_knots < 0:
        raise ValueError("Ocean current speed cannot be negative.")

    if wave_height_m < 0:
        raise ValueError("Wave height cannot be negative.")

    if current_speed_knots >= 3 or wave_height_m >= 6:
        return "CRITICAL"

    elif current_speed_knots >= 2 or wave_height_m >= 4:
        return "HIGH"

    elif current_speed_knots >= 1 or wave_height_m >= 2:
        return "MEDIUM"

    else:
        return "LOW"

def calculate_overall_risk(ice_risk, weather_risk, ocean_risk):
    """
    Calculate overall navigation risk from ice, weather, and ocean risks.
    Demo/simulation rule-based logic only.
    """

    risk_levels = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    risks = [ice_risk, weather_risk, ocean_risk]

    for risk in risks:
        if risk not in risk_levels:
            raise ValueError(
                "Risk level must be LOW, MEDIUM, HIGH, or CRITICAL."
            )

    return max(risks, key=lambda risk: risk_levels[risk])

def calculate_safety_score(overall_risk):
    """
    Convert overall navigation risk into a safety score from 0 to 100.
    Demo/simulation rule-based logic only.
    """

    safety_scores = {
        "LOW": 100,
        "MEDIUM": 70,
        "HIGH": 40,
        "CRITICAL": 10
    }

    if overall_risk not in safety_scores:
        raise ValueError(
            "Overall risk must be LOW, MEDIUM, HIGH, or CRITICAL."
        )

    return safety_scores[overall_risk]

def generate_warnings(
    ice_risk,
    weather_risk,
    ocean_risk
):
    """
    Generate important navigation warnings.
    Demo/simulation rule-based logic only.
    """

    warnings = []

    if ice_risk == "CRITICAL":
        warnings.append("CRITICAL: Extremely high ice navigation risk.")
    elif ice_risk == "HIGH":
        warnings.append("WARNING: High iceberg/sea-ice risk.")
    elif ice_risk == "MEDIUM":
        warnings.append("CAUTION: Moderate ice navigation risk.")

    if weather_risk == "CRITICAL":
        warnings.append("CRITICAL: Severe weather conditions.")
    elif weather_risk == "HIGH":
        warnings.append("WARNING: High weather-related risk.")
    elif weather_risk == "MEDIUM":
        warnings.append("CAUTION: Moderate weather conditions.")

    if ocean_risk == "CRITICAL":
        warnings.append("CRITICAL: Dangerous ocean conditions.")
    elif ocean_risk == "HIGH":
        warnings.append("WARNING: High ocean-condition risk.")
    elif ocean_risk == "MEDIUM":
        warnings.append("CAUTION: Moderate ocean conditions.")

    if not warnings:
        warnings.append("No major navigation warnings.")

    return warnings

def generate_risk_zones():
    """
    Generate map-ready risk zone data.
    Demo/simulation data only.
    """

    return [
        {
            "zone": "Zone A",
            "risk": "CRITICAL",
            "latitude": -64.5,
            "longitude": -62.3
        },
        {
            "zone": "Zone B",
            "risk": "HIGH",
            "latitude": -65.1,
            "longitude": -61.8
        },
        {
            "zone": "Zone C",
            "risk": "MEDIUM",
            "latitude": -66.0,
            "longitude": -60.5
        },
        {
            "zone": "Zone D",
            "risk": "LOW",
            "latitude": -67.2,
            "longitude": -59.7
        }
    ]
