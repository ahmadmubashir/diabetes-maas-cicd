# backend/agents/evidence_agent.py
from backend.rag.retriever import retrieve_evidence

def evidence_agent(state):
    # Build query that includes risk factors for better retrieval
    query = f"""
    Diabetes Risk Level: {state['risk_level']}
    Risk Factors: {', '.join(state['risk_factors'])}
    Clinical guidelines for diabetes prevention and management.
    """
    evidence = retrieve_evidence(query)
    state["evidence"] = evidence if evidence else "No specific guidelines retrieved."
    return state