from database.database import SessionLocal
from database.models import Employee
from typing import Dict, Any

def get_employee_metadata(name: str):
    db = SessionLocal()
    try:
        # Only fetch metadata needed for RBAC
        return db.query(Employee).filter(Employee.name.ilike(f"%{name}%")).first()
    finally:
        db.close()

def authorization_agent(state: Dict[str, Any]):
    current_user = state.get("current_user")
    trace = state.get("trace", [])
    
    if not current_user:
        auth_msg = "Access Denied: No active identity found."
        trace.append(f"Authorization Agent → Decision: DENIED | Reason: No user session.")
        return {"access_granted": False, "auth_message": auth_msg, "trace": trace}

    user_name = current_user.get("name")
    user_role = current_user.get("role")
    user_dept = current_user.get("department", "").upper()
    user_id = current_user.get("employee_id")

    employee_name = state.get("employee_name")
    department_name = state.get("department_name", "").upper() if state.get("department_name") else None
    
    trace.append(f"Authorization Agent → User: {user_name} | Role: {user_role} | Dept: {user_dept}")

    access_granted = False
    reason = ""

    # CEO & HR HEAD: Elevated Permissions
    if user_role == 'CEO':
        access_granted = True
        reason = "CEO has full organization visibility."
    
    elif user_role == 'HR_HEAD':
        target = get_employee_metadata(employee_name) if employee_name else None
        if target and target.role == 'CEO':
            access_granted = False
            reason = "HR Head cannot access Executive (CEO) data."
        else:
            access_granted = True
            reason = "HR Head has departmental authority for all other staff."

    # DEPT DIRECTOR: Strict Departmental Boundary
    elif user_role == 'DEPT_DIRECTOR':
        if employee_name:
            target = get_employee_metadata(employee_name)
            if target and target.department.upper() == user_dept:
                access_granted = True
                reason = f"Target is within the {user_dept} department."
            else:
                access_granted = False
                reason = f"Cross-department access is not permitted. User is in {user_dept}, Target is in {target.department if target else 'Unknown'}."
        elif department_name:
            if department_name == user_dept:
                access_granted = True
                reason = f"Authorized for {user_dept} analytics."
            else:
                access_granted = False
                reason = f"Access denied. Directors are restricted to {user_dept} analytics."

    # MANAGER: Direct Reports Only
    elif user_role == 'MANAGER':
        if employee_name:
            target = get_employee_metadata(employee_name)
            if target:
                if target.employee_id == user_id:
                    access_granted = True
                    reason = "Self-access permitted."
                elif target.manager_id == user_id:
                    access_granted = True
                    reason = "Target is a direct report."
                else:
                    access_granted = False
                    reason = f"Target {target.name} does not report to you."
            else:
                access_granted = False
                reason = "Target employee not found."
        else:
            access_granted = False
            reason = "Managers cannot access wide-scale analytics."

    # EMPLOYEE: Self Only
    elif user_role == 'EMPLOYEE':
        if employee_name:
            target = get_employee_metadata(employee_name)
            if target and target.employee_id == user_id:
                access_granted = True
                reason = "Self-access permitted."
            else:
                access_granted = False
                reason = "Employees can only access their own profile."
        else:
             access_granted = False
             reason = "Employees have no analytics permissions."

    status = "ACCESS GRANTED" if access_granted else "ACCESS DENIED"
    trace.append(f"Authorization Agent → Decision: {status}")
    trace.append(f"Authorization Agent → Reason: {reason}")

    return {
        "access_granted": access_granted,
        "auth_message": reason if not access_granted else f"Authorized: {reason}",
        "trace": trace
    }
