def route_intent(state):

    intents = state["intents"]

    if any(
        intent in [
            "employee_details",
            "salary_lookup",
            "compare_salary",
            "manager_lookup",
            "promotion_analysis"
        ]
        for intent in intents
    ):
        return "employee_lookup_agent"

    if "department_info" in intents:
        return "department_agent"

    return "employee_lookup_agent"