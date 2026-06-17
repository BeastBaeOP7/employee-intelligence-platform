from config.github_models_llm import get_llm
from schemas.router_output import RouterOutput

llm = get_llm()

structured_llm = llm.with_structured_output(
    RouterOutput
)


def controller_agent(state):
    query = state["user_query"]
    current_employee_context = state.get("current_user", {})
    user_name = current_employee_context.get("name", "Unknown User")

    previous_employee = state.get("employee_name")
    previous_dept = state.get("department_name")

    prompt = f"""
You are an Employee Analytics Router.

Current User: {user_name}

Your goal: Extract intents, employee_name, and department_name.

CRITICAL RULES:
1. If the user mentions a NEW person by name, extract that name into 'employee_name'.
2. Only use the concept of "me/my" if the user actually says "me", "my", "mine", etc. (Resolve to '{user_name}').
3. If the user mentions a specific department, extract it.

Available intents:
- employee_details
- salary_lookup
- compare_salary
- manager_lookup
- department_info
- promotion_analysis
- export_excel
- team_lookup
- org_analytics

Examples:
- "Who reports to Mark Tech?" -> intents=["team_lookup"], employee_name="Mark Tech"
- "Who manages Ryan Cooper?" -> intents=["manager_lookup"], employee_name="Ryan Cooper"
- "Show HR department" -> intents=["department_info"], department_name="HR"
- "Show all department statistics" -> intents=["org_analytics"]
- "Who are the department heads?" -> intents=["org_analytics"]

User Query:
{query}
"""

    result = structured_llm.invoke(prompt)

    query_lower = query.lower()

    # Force org analytics for company-wide exports
    if (
        "company report" in query_lower
        or "organization report" in query_lower
        or "full company report" in query_lower
        or "complete company report" in query_lower
    ):
        if "org_analytics" not in result.intents:
            result.intents.append("org_analytics")

    extracted_employee = result.employee_name
    extracted_dept = result.department_name

    final_employee = extracted_employee
    final_dept = extracted_dept

    is_continuity_query = any(
        word in query_lower
        for word in [
            "him",
            "her",
            "they",
            "them",
            "his",
            "hers",
            "their",
            "that",
            "this",
            "it",
        ]
    )

    if not extracted_employee and is_continuity_query:
        final_employee = previous_employee

    if not extracted_dept and is_continuity_query:
        final_dept = previous_dept

    print("\n[DEBUG] Controller Agent")
    print(f" > Raw Query: {query}")
    print(f" > Extracted Intents: {result.intents}")
    print(f" > Extracted Employee: {extracted_employee} (Previous: {previous_employee})")
    print(f" > Extracted Dept: {extracted_dept} (Previous: {previous_dept})")
    print(f" > FINAL TARGET: {final_employee or final_dept or 'Organization'}")
    print("-" * 30)

    trace = state.get("trace", [])
    trace.append(
        f"Controller Agent → Intent={result.intents} | Targets: Employee='{final_employee}', Dept='{final_dept}'"
    )

    return {
        "intents": result.intents,
        "employee_name": final_employee,
        "department_name": final_dept,
        "trace": trace,
    }