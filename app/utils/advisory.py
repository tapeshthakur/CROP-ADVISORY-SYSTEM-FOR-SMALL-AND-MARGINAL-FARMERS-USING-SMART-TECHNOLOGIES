from typing import Dict


def fertilizer_recommendation(nitrogen: float, phosphorus: float, potassium: float) -> str:
    recommendations = []
    if nitrogen < 40:
        recommendations.append("Apply urea or compost to improve nitrogen levels.")
    if phosphorus < 40:
        recommendations.append("Use DAP or bone meal to increase phosphorus.")
    if potassium < 40:
        recommendations.append("Add potash or wood ash for potassium boost.")

    if not recommendations:
        return "Soil nutrients are balanced. Maintain with organic compost."

    return " ".join(recommendations)


def pest_disease_advisory(crop: str, humidity: float, season: str) -> str:
    crop = crop.lower()
    if humidity > 80:
        return (
            "High humidity detected. Monitor for fungal diseases like leaf blight "
            "and use neem-based bio-fungicides if symptoms appear."
        )

    if crop in {"rice", "wheat"}:
        return "Watch for stem borers and apply pheromone traps if needed."

    if season.lower() == "summer":
        return "Check for aphids and mites. Encourage natural predators."

    return "Regular field scouting is advised for early pest detection."


def build_explanation(crop: str, fertilizer: str, weather: Dict[str, float]) -> str:
    return (
        f"Based on your soil nutrients and current weather, {crop} is a suitable crop. "
        f"Weather shows temperature {weather['temperature']}°C with {weather['rainfall']}mm rainfall. "
        f"Fertilizer guidance: {fertilizer}"
    )
