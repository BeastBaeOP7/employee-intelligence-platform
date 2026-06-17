from tools.department_api_tool import get_department_stats
from tools.salary_analysis_tool import compare_salary


def analytics_agent(state):

    employee = state["employee_data"]

    stats = get_department_stats(
        employee["department"]
    )

    salary_comparison = compare_salary(
        employee,
        stats
    )

    return {
        "department_stats": stats,
        "salary_analysis": salary_comparison
    }