# backend/agents/lifestyle_agent.py
def lifestyle_agent(state):
    factors = state["risk_factors"]
    recommendations = []

    if "High BMI" in factors:
        recommendations.append("• Aim for 5–10% weight loss through portion control and daily walking.")
    if "Elevated HbA1c" in factors or "Elevated Blood Glucose" in factors:
        recommendations.append("• Reduce refined carbs and sugars; increase fiber (vegetables, whole grains).")
    if "Hypertension" in factors:
        recommendations.append("• Limit sodium to <2300 mg/day; consider DASH diet.")
    if not recommendations:
        recommendations.append("• Continue balanced diet: lean protein, healthy fats, complex carbohydrates.")

    recommendations.append("• Physical activity: 150 min/week moderate exercise (brisk walking, cycling).")
    state["lifestyle_advice"] = "\n".join(recommendations)
    return state