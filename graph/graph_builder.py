from langgraph.graph import StateGraph, END

from graph.state import AgentState

from agents.controller_agent import controller_agent
from agents.authorization_agent import authorization_agent
from agents.retrieval_agent import retrieval_agent
from agents.analysis_agent import analysis_agent


# ==========================================================
# Denial Node
# ==========================================================

def denial_response(state):

    print("\n========== DENIAL NODE ==========")
    print("Authorization Failed")
    print(f"Reason : {state.get('auth_message')}")
    print("=================================\n")

    trace = state.get("trace", [])
    trace.append("Denial Node → Request terminated due to failed authorization.")

    return {
        "analysis": f"🛑 **Access Denied**\n\n{state.get('auth_message')}",
        "trace": trace,
    }


# ==========================================================
# Router
# ==========================================================

def route_after_authorization(state):

    if state.get("access_granted", False):
        return "retrieval_agent"

    return "denial_response"


# ==========================================================
# Graph Builder
# ==========================================================

def build_graph():

    print("\n========== BUILDING LANGGRAPH ==========")

    builder = StateGraph(AgentState)

    # ------------------------------------------------------
    # Register Nodes
    # ------------------------------------------------------

    builder.add_node("controller_agent", controller_agent)
    builder.add_node("authorization_agent", authorization_agent)
    builder.add_node("retrieval_agent", retrieval_agent)
    builder.add_node("analysis_agent", analysis_agent)
    builder.add_node("denial_response", denial_response)

    print("✓ Registered Controller Agent")
    print("✓ Registered Authorization Agent")
    print("✓ Registered Retrieval Agent")
    print("✓ Registered Analysis Agent")
    print("✓ Registered Denial Node")

    # ------------------------------------------------------
    # Entry Point
    # ------------------------------------------------------

    builder.set_entry_point("controller_agent")

    # ------------------------------------------------------
    # Controller → Authorization
    # ------------------------------------------------------

    builder.add_edge(
        "controller_agent",
        "authorization_agent",
    )

    # ------------------------------------------------------
    # Authorization Routing
    # ------------------------------------------------------

    builder.add_conditional_edges(
        "authorization_agent",
        route_after_authorization,
        {
            "retrieval_agent": "retrieval_agent",
            "denial_response": "denial_response",
        },
    )

    # ------------------------------------------------------
    # Authorized Flow
    # ------------------------------------------------------

    builder.add_edge(
        "retrieval_agent",
        "analysis_agent",
    )

    builder.add_edge(
        "analysis_agent",
        END,
    )

    # ------------------------------------------------------
    # Denied Flow
    # ------------------------------------------------------

    builder.add_edge(
        "denial_response",
        END,
    )

    print("\nGraph Flow")
    print("--------------------------------")
    print("Controller")
    print("   ↓")
    print("Authorization")
    print("   ├── DENIED → Denial Node → END")
    print("   └── ALLOWED → Retrieval → Analysis → END")
    print("--------------------------------")
    print("Graph compiled successfully.")
    print("==========================================\n")

    return builder.compile()