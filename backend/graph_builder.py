# backend/graph_builder.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from backend.agents.evidence_agent import evidence_agent
from backend.agents.explanation_agent import generate_explanation
from backend.agents.risk_agent import risk_agent
from backend.agents.lifestyle_agent import lifestyle_agent
from backend.agents.monitoring_agent import monitoring_agent
from backend.agents.summary_agent import summary_agent

class AgentState(TypedDict):
    probability: float
    risk_level: str
    risk_factors: List[str]
    evidence: str
    explanation: str
    risk_advice: str
    lifestyle_advice: str
    monitoring_advice: str
    summary: str

# Define node functions
def evidence_node(state: AgentState) -> AgentState:
    return evidence_agent(state)

def explanation_node(state: AgentState) -> AgentState:
    explanation = generate_explanation(
        probability=state["probability"],
        risk_level=state["risk_level"],
        risk_factors=state["risk_factors"],
        evidence=state["evidence"]
    )
    state["explanation"] = explanation
    return state

def risk_node(state: AgentState) -> AgentState:
    return risk_agent(state)

def lifestyle_node(state: AgentState) -> AgentState:
    return lifestyle_agent(state)

def monitoring_node(state: AgentState) -> AgentState:
    return monitoring_agent(state)

def summary_node(state: AgentState) -> AgentState:
    return summary_agent(state)

# Build graph
builder = StateGraph(AgentState)
builder.add_node("evidence_agent", evidence_node)
builder.add_node("explanation_agent", explanation_node)
builder.add_node("risk_agent", risk_node)
builder.add_node("lifestyle_agent", lifestyle_node)
builder.add_node("monitoring_agent", monitoring_node)
builder.add_node("summary_agent", summary_node)

builder.set_entry_point("evidence_agent")
builder.add_edge("evidence_agent", "explanation_agent")
builder.add_edge("explanation_agent", "risk_agent")
builder.add_edge("risk_agent", "lifestyle_agent")
builder.add_edge("lifestyle_agent", "monitoring_agent")
builder.add_edge("monitoring_agent", "summary_agent")
builder.add_edge("summary_agent", END)

graph = builder.compile()