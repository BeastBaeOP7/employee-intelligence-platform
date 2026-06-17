from langgraph.graph import StateGraph, END
from graph.state import AgentState

from agents.controller_agent import controller_agent
from agents.authorization_agent import authorization_agent
from agents.team_lookup_agent import team_lookup_agent
from agents.employee_lookup_agent import employee_lookup_agent
from agents.department_agent import department_agent
from agents.analysis_agent import analysis_agent
from agents.excel_export_agent import excel_export_agent

def route_after_auth(state):
    if not state.get("access_granted", False):
        return "denial_response"
    return "team_lookup_agent"

def denial_response(state):
    trace = state.get("trace", [])
    trace.append("Denial Handler → Terminal state reached. Blocking data retrieval.")
    return {
        "analysis": f"🛑 **Access Denied**\n\n{state.get('auth_message')}",
        "trace": trace
    }

def route_after_analysis(state):
    intents = state.get("intents", [])
    print("AFTER ANALYSIS")
    print("INTENTS:", state.get("intents"))
    print("ACCESS:", state.get("access_granted"))
    # Only export if access was granted
    if "export_excel" in intents and state.get("access_granted"):
        return "excel_export_agent"
    return END

def route_after_analysis(state):

    print("AFTER ANALYSIS")
    print("INTENTS =", state.get("intents"))
    print("ACCESS =", state.get("access_granted"))

    intents = state.get("intents", [])

    if "export_excel" in intents and state.get("access_granted"):
        return "excel_export_agent"

    return END
    
def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("controller_agent", controller_agent)
    builder.add_node("authorization_agent", authorization_agent)
    builder.add_node("denial_response", denial_response)
    builder.add_node("team_lookup_agent", team_lookup_agent)
    builder.add_node("employee_lookup_agent", employee_lookup_agent)
    builder.add_node("department_agent", department_agent)
    builder.add_node("analysis_agent", analysis_agent)
    builder.add_node("excel_export_agent", excel_export_agent)

    builder.set_entry_point("controller_agent")

    builder.add_edge("controller_agent", "authorization_agent")

    builder.add_conditional_edges(
        "authorization_agent",
        route_after_auth,
        {
            "denial_response": "denial_response",
            "team_lookup_agent": "team_lookup_agent"
        }
    )

    # Denial response is terminal for data agents
    builder.add_edge("denial_response", END)

    builder.add_edge("team_lookup_agent", "employee_lookup_agent")
    builder.add_edge("employee_lookup_agent", "department_agent")
    builder.add_edge("department_agent", "analysis_agent")

    builder.add_conditional_edges(
        "analysis_agent",
        route_after_analysis,
        {
            "excel_export_agent": "excel_export_agent",
            "__end__": END
        }
    )

    builder.add_edge("excel_export_agent", END)

    return builder.compile()