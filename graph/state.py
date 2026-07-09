from typing import Optional, TypedDict


class AgentState(TypedDict):
    """
    Shared state passed between all LangGraph agents.
    """

    # --------------------------------------------------
    # User Input
    # --------------------------------------------------

    user_query: str
    current_user: Optional[dict]

    # --------------------------------------------------
    # Controller Output
    # --------------------------------------------------

    intents: list[str]
    employee_name: Optional[str]
    department_name: Optional[str]

    # --------------------------------------------------
    # Authorization Output
    # --------------------------------------------------

    access_granted: bool
    auth_message: Optional[str]

    # --------------------------------------------------
    # Retrieval Output
    # --------------------------------------------------

    employee_data: Optional[dict]
    department_stats: Optional[dict]
    team_data: Optional[dict]
    organization_data: Optional[dict]
    promotion_candidates: Optional[list]

    # --------------------------------------------------
    # Analysis Output
    # --------------------------------------------------

    analysis: Optional[str]

    # --------------------------------------------------
    # Debug Trace
    # --------------------------------------------------

    trace: list[str]