# backend/agents/monitoring_agent.py
def monitoring_agent(state):
    prob = state["probability"]
    if prob > 0.7:
        plan = "• Check fasting glucose weekly.\n• HbA1c every 3 months.\n• Annual eye and foot exams."
    elif prob > 0.4:
        plan = "• Monitor fasting glucose monthly.\n• HbA1c every 6 months.\n• Annual check‑up."
    else:
        plan = "• Annual glucose screening.\n• HbA1c every 1‑2 years if no symptoms."
    state["monitoring_advice"] = plan
    return state