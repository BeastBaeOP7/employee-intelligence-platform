from config.github_models_llm import get_llm
from schemas.router_output import RouterOutput

llm = get_llm()

structured_llm = llm.with_structured_output(RouterOutput)


def controller_agent(state):
    query = state["user_query"]

    current_user = state.get("current_user", {})
    user_name = current_user.get("name", "Unknown User")

    previous_employee = state.get("employee_name")
    previous_department = state.get("department_name")

    prompt = f"""
You are the Controller Agent of an Employee Analytics System.

Your ONLY responsibility is routing.

Return:
- intents
- employee_name
- department_name

-------------------------
AVAILABLE INTENTS
-------------------------

employee_details
salary_lookup
compare_salary
manager_lookup
department_info
promotion_analysis
export_excel
team_lookup
org_analytics

-------------------------
RULES
-------------------------

1. Extract the employee name if one is mentioned.

2. Extract the department if one is mentioned.

3. If the user says "me", "my", or "mine",
use "{user_name}" as employee_name.

4. Return ONLY intents from the list above.

5. A company-wide report, organization report,
department heads, company statistics,
organization analytics or organization chart
should use org_analytics.

-------------------------
EXAMPLES
-------------------------

User:
Tell me about Ryan Cooper

Output:
employee_details
employee_name="Ryan Cooper"

-------------------------

User:
Who manages Ryan Cooper?

Output:
manager_lookup
employee_name="Ryan Cooper"

-------------------------

User:
Who reports to Ryan Cooper?

Output:
team_lookup
employee_name="Ryan Cooper"

-------------------------

User:
Show HR department statistics

Output:
department_info
department_name="HR"

-------------------------

User:
Compare Ryan Cooper's salary with Emma Wilson

Output:
compare_salary
employee_name="Ryan Cooper"

-------------------------

User:
Show promotion candidates

Output:
promotion_analysis

-------------------------

User:
Generate company report

Output:
org_analytics

-------------------------

User:
Show all department heads

Output:
org_analytics

-------------------------

User:
Export HR report to Excel

Output:
department_info
export_excel
department_name="HR"

-------------------------

User Query:
{query}
"""

    result = structured_llm.invoke(prompt)

    extracted_employee = result.employee_name
    extracted_department = result.department_name

    followup_words = {
        "him",
        "her",
        "his",
        "hers",
        "them",
        "their",
        "they",
        "that",
        "this",
        "it",
        "same",
        "previous",
        "above",
    }

    query_lower = query.lower()

    is_followup = any(word in query_lower for word in followup_words)

    final_employee = extracted_employee
    final_department = extracted_department

    if is_followup:

        if not final_employee:
            final_employee = previous_employee

        if not final_department:
            final_department = previous_department

    print("\n==============================")
    print("CONTROLLER AGENT")
    print("==============================")
    print(f"Query      : {query}")
    print(f"Intents    : {result.intents}")
    print(f"Employee   : {final_employee}")
    print(f"Department : {final_department}")
    print("==============================\n")

    trace = state.get("trace", [])

    trace.append(
        f"Controller → intents={result.intents}, employee={final_employee}, department={final_department}"
    )

    return {
        "intents": result.intents,
        "employee_name": final_employee,
        "department_name": final_department,
        "trace": trace,
    }