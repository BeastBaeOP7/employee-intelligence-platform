from copy import deepcopy

# Never allow these fields to reach the LLM
ALWAYS_REMOVE = {
    "password",
    "credit_card",
    "api_key",
    "access_token",
    "session_token",
    "secret",
}

ROLE_FIELD_PERMISSIONS = {

    # CEO sees everything
    "CEO": None,

    # HR
    "HR_HEAD": {
        "employee_id",
        "name",
        "department",
        "designation",
        "role",
        "salary",
        "experience_years",
        "manager_id",
        "location",
        "performance_rating",
        "join_date",
        "email",
        "manager_name",
        "manager_designation",
        "manager_data"
    },

    # Managers
    "MANAGER": {
        "employee_id",
        "name",
        "department",
        "designation",
        "role",
        "salary",
        "experience_years",
        "manager_id",
        "location",
        "performance_rating",
        "join_date",
        "manager_name",
        "manager_designation",
        "manager_data"
    },

    # Employees
    "EMPLOYEE": {
        "employee_id",
        "name",
        "department",
        "designation",
        "role",
        "experience_years",
        "location",
        "performance_rating",
        "join_date",
        "manager_name",
        "manager_designation"
    }
}


def filter_employee(employee: dict, role: str):

    if employee is None:
        return None
    
    employee = {
        k: v
        for k, v in employee.items()
        if k not in ALWAYS_REMOVE
    }

    allowed = ROLE_FIELD_PERMISSIONS.get(role)
    # CEO gets every detail
    if allowed is None:
        return deepcopy(employee)

    return {
        k: v
        for k, v in employee.items()
        if k in allowed
    }