from typing import Dict, Optional


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


def build_explanation(
    crop: str, fertilizer: str, weather: Dict[str, float], confidence: Optional[float]
) -> str:
    confidence_text = (
        f"The model confidence is {confidence * 100:.1f}%. " if confidence is not None else ""
    )
    return (
        f"{crop.title()} is recommended because the entered soil nutrients and rainfall pattern "
        f"match similar historical samples from the training data. {confidence_text}"
        f"Current weather is {weather['temperature']}°C with {weather['rainfall']}mm rainfall and "
        f"{weather['humidity']}% humidity. Fertilizer guidance: {fertilizer}"
    )
