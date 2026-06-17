from database.database import SessionLocal
from database.models import Employee
from typing import Dict, Any

def get_direct_reports(manager_id):
    db = SessionLocal()
    try:
        return db.query(Employee).filter(Employee.manager_id == manager_id).all()
    finally:
        db.close()

def build_tree_recursive(manager_id, level=0):
    reports = get_direct_reports(manager_id)
    tree_str = ""
    for r in reports:
        indent = "│   " * level
        tree_str += f"{indent}├── {r.name} ({r.designation})\n"
        tree_str += build_tree_recursive(r.employee_id, level + 1)
    return tree_str

def team_lookup_agent(state: Dict[str, Any]):
    intents = state.get("intents", [])
    trace = state.get("trace", [])
    
    # We trigger if team_lookup or org_analytics or department_info is present
    if not any(i in intents for i in ["team_lookup", "org_analytics", "org_chart", "department_info"]):
        return state

    employee_name = state.get("employee_name")
    department_name = state.get("department_name")
    current_user = state.get("current_user")
    
    db = SessionLocal()
    try:
        target_employee = None
        
        # Priority 1: Specific Employee
        if employee_name:
             target_employee = db.query(Employee).filter(Employee.name.ilike(f"%{employee_name}%")).first()
        
        # Priority 2: Department Head (if dept_info requested)
        if not target_employee and department_name:
             target_employee = db.query(Employee).filter(
                 Employee.department.ilike(f"{department_name}"),
                 Employee.role.in_(['DEPT_DIRECTOR', 'HR_HEAD', 'CEO'])
             ).order_by(Employee.salary.desc()).first()
             if target_employee:
                 trace.append(f"Team Lookup Agent → Resolved hierarchy root to Department Head: {target_employee.name}")

        # Priority 3: Current User (fallback for team_lookup)
        if not target_employee and current_user:
             target_employee = db.query(Employee).filter(Employee.employee_id == current_user['employee_id']).first()
        
        if not target_employee:
            trace.append("Team Lookup Agent → No suitable target found for hierarchy building.")
            return {"trace": trace}

        trace.append(f"Team Lookup Agent → Building recursive hierarchy from {target_employee.name}")
        
        team_data = {}
        # Recursive Tree
        full_tree = f"{target_employee.name} ({target_employee.designation})\n"
        full_tree += build_tree_recursive(target_employee.employee_id)
        team_data["full_hierarchy"] = full_tree
        
        # Direct Reports
        reports = get_direct_reports(target_employee.employee_id)
        team_data["direct_reports"] = [{"name": r.name, "role": r.role, "designation": r.designation} for r in reports]
        
        return {
            "team_data": team_data,
            "trace": trace
        }
    finally:
        db.close()

