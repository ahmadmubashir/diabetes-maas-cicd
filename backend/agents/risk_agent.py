# backend/agents/risk_agent.py
def risk_agent(state):
    prob = state["probability"]
    risk = state["risk_level"]
    factors = state["risk_factors"]

    if prob > 0.7:
        advice = f"⚠️ High risk ({risk}). Immediate clinical consultation strongly advised."
    elif prob > 0.4:
        advice = f"⚠️ Moderate risk ({risk}). Schedule a check‑up within 3 months."
    else:
        advice = f"✅ Low risk ({risk}). Maintain healthy habits."

    if factors:
        advice += f" Key concerns: {', '.join(factors)}."

    state["risk_advice"] = advice
    return state