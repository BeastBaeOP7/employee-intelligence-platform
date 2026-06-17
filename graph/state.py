from typing import TypedDict, Optional


class AgentState(TypedDict):
    user_query: str
    current_user: Optional[dict]  # Active identity for the session

    intents: list[str]
    employee_name: Optional[str]
    department_name: Optional[str]

    access_granted: bool
    auth_message: Optional[str]

    employee_data: Optional[dict]
    department_stats: Optional[dict]
    team_data: Optional[dict]
    organization_data: Optional[dict]

    analysis: Optional[str]
    excel_path: Optional[str]

    trace: list
    