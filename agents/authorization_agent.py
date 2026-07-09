from typing import Dict, Any

from database.database import SessionLocal
from database.models import Employee


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def get_target_employee(name: str):
    """Returns the employee object used only for authorization checks."""
    if not name:
        return None

    db = SessionLocal()
    try:
        return (
            db.query(Employee)
            .filter(Employee.name.ilike(f"%{name}%"))
            .first()
        )
    finally:
        db.close()


# ------------------------------------------------------------------
# Authorization Agent
# ------------------------------------------------------------------

def authorization_agent(state: Dict[str, Any]):

    current_user = state.get("current_user")
    trace = state.get("trace", [])

    print("\n========== AUTHORIZATION AGENT ==========")

    if not current_user:
        print("No authenticated user.")
        print("========================================")

        trace.append(
            "Authorization Agent → DENIED | No authenticated user."
        )

        return {
            "access_granted": False,
            "auth_message": "Access Denied: No active identity found.",
            "trace": trace,
        }

    employee_name = state.get("employee_name")
    department_name = state.get("department_name")

    print(f"Current User : {current_user['name']}")
    print(f"Role         : {current_user['role']}")
    print(f"Employee     : {employee_name}")
    print(f"Department   : {department_name}")
    print("----------------------------------------")

    user_role = current_user["role"]
    user_id = current_user["employee_id"]
    user_department = current_user.get("department", "").upper()

    target = get_target_employee(employee_name)

    access_granted = False
    reason = ""

    # ==========================================================
    # CEO
    # ==========================================================

    if user_role == "CEO":

        access_granted = True
        reason = "CEO has organization-wide access."

    # ==========================================================
    # HR HEAD
    # ==========================================================

    elif user_role == "HR_HEAD":

        if target and target.role == "CEO":
            access_granted = False
            reason = "HR Head cannot access CEO information."

        else:
            access_granted = True
            reason = "HR Head has access to all employees except CEO."

    # ==========================================================
    # DEPARTMENT DIRECTOR
    # ==========================================================

    elif user_role == "DEPT_DIRECTOR":

        if target:

            if target.department.upper() == user_department:
                access_granted = True
                reason = "Target employee belongs to same department."

            else:
                access_granted = False
                reason = (
                    f"Cross-department access denied "
                    f"({user_department} → {target.department})."
                )

        elif department_name:

            if department_name.upper() == user_department:
                access_granted = True
                reason = "Department analytics allowed."

            else:
                access_granted = False
                reason = "Directors can access only their own department."

        else:
            access_granted = False
            reason = "Department not specified."

    # ==========================================================
    # MANAGER
    # ==========================================================

    elif user_role == "MANAGER":

        if target:

            if target.employee_id == user_id:
                access_granted = True
                reason = "Self access."

            elif target.manager_id == user_id:
                access_granted = True
                reason = "Employee is your direct report."

            else:
                access_granted = False
                reason = "Employee is not your direct report."

        else:
            access_granted = False
            reason = "Employee not found."

    # ==========================================================
    # EMPLOYEE
    # ==========================================================

    elif user_role == "EMPLOYEE":

        if target:

            if target.employee_id == user_id:
                access_granted = True
                reason = "Self access."

            else:
                access_granted = False
                reason = "Employees may only access their own profile."

        else:
            access_granted = False
            reason = "Employee not found."

    # ==========================================================
    # Unknown Role
    # ==========================================================

    else:

        access_granted = False
        reason = "Unknown role."

    # ------------------------------------------------------------------

    decision = "GRANTED" if access_granted else "DENIED"

    print("\nDecision")
    print("------------------------")
    print(f"Access : {decision}")
    print(f"Reason : {reason}")
    print("========================================\n")

    trace.append(
        f"Authorization Agent → {decision} | {reason}"
    )

    return {
        "access_granted": access_granted,
        "auth_message": (
            f"Authorized: {reason}"
            if access_granted
            else reason
        ),
        "trace": trace,
    }