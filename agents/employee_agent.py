from tools.employee_api_tool import get_employee


def employee_agent(state):

    employee = get_employee(
        state["employee_id"]
    )

    return {
        "employee_data": employee
    }