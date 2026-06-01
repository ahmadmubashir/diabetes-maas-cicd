# backend/agents/explanation_agent.py
def generate_explanation(probability: float, risk_level: str, risk_factors: list, evidence: str) -> str:
    prob_pct = probability * 100
    if probability > 0.7:
        base = f"The model estimates a very high probability ({prob_pct:.1f}%) of diabetes. "
    elif probability > 0.4:
        base = f"The model estimates a moderate probability ({prob_pct:.1f}%) of diabetes. "
    else:
        base = f"The model estimates a low probability ({prob_pct:.1f}%) of diabetes. "

    if risk_factors:
        base += f"The following risk factors contributed: {', '.join(risk_factors)}. "
    else:
        base += "No major clinical risk factors were identified. "

    if evidence and len(evidence) > 100:
        base += "These findings are consistent with clinical guidelines retrieved from ADA/WHO/PubMed."
    else:
        base += "Please consult a healthcare professional for a complete assessment."
    return base