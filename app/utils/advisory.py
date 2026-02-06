from typing import Dict


def get_fertilizer_advisory(
    nitrogen: float,
    phosphorus: float,
    potassium: float
) -> str:
    """
    Provides fertilizer recommendations based on soil nutrient values.
    """
    recommendations = []

    if nitrogen < 40:
        recommendations.append(
            "Apply urea or well-decomposed compost to improve nitrogen levels."
        )

    if phosphorus < 40:
        recommendations.append(
            "Use DAP or bone meal to increase phosphorus content in the soil."
        )

    if potassium < 40:
        recommendations.append(
            "Add potash or wood ash to boost potassium levels."
        )

    if not recommendations:
        return "Soil nutrients are balanced. Maintain fertility using organic compost."

    return " ".join(recommendations)


def get_pest_advisory(
    crop: str,
    humidity: float,
    season: str
) -> str:
    """
    Gives pest and disease advisory based on crop, humidity, and season.
    """
    crop = crop.lower()
    season = season.lower()

    if humidity > 80:
        return (
            "High humidity detected. Risk of fungal diseases such as leaf blight. "
            "Use neem-based bio-fungicides if symptoms appear."
        )

    if crop in {"rice", "wheat"}:
        return (
            "Common pests include stem borers. Monitor fields and use pheromone traps if required."
        )

    if season == "summer":
        return (
            "Dry summer conditions may cause aphids and mites. Encourage natural predators."
        )

    return "Regular field scouting is advised for early pest and disease detection."


def get_crop_advisory(
    crop: str,
    fertilizer_advice: str,
    weather: Dict[str, float]
) -> str:
    """
    Builds a final crop advisory explanation combining weather and fertilizer guidance.
    """
    temperature = weather.get("temperature", "N/A")
    rainfall = weather.get("rainfall", "N/A")

    return (
        f"{crop.capitalize()} is suitable under current conditions. "
        f"Weather forecast indicates a temperature of {temperature}°C "
        f"and expected rainfall of {rainfall} mm. "
        f"Fertilizer recommendation: {fertilizer_advice}"
    )
