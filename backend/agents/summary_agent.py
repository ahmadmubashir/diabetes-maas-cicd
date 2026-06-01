# backend/agents/summary_agent.py
def summary_agent(state):
    evidence_preview = state["evidence"][:500] + ("..." if len(state["evidence"]) > 500 else "")
    summary = f"""
### LangGraph Agent Report

**Risk Assessment**  
{state['risk_advice']}

**Why this prediction?**  
{state['explanation']}

**Evidence from Guidelines**  
{evidence_preview}

**Lifestyle Recommendations**  
{state['lifestyle_advice']}

**Monitoring Plan**  
{state['monitoring_advice']}
"""
    state["summary"] = summary
    return state