"""
Retrieval Agent — Single agent responsible for ALL data retrieval.

Responsibilities:
- Employee lookup and manager resolution
- Team hierarchy and direct reports
- Department statistics and organization-wide stats
- Promotion candidates
- No LLM reasoning — pure data retrieval only.
"""

import requests
from typing import Dict, Any
from security_guardrails.rbac_filter import filter_employee

from database.database import SessionLocal
from database.models import Employee
from utils.employee_utils import get_manager_data
from tools.department_api_tool import (
    get_department_stats,
    get_organization_stats,
    get_department_heads,
    get_all_department_stats,
    get_promotion_candidates,
    get_top_paid_employees,
)


# ---------------------------------------------------------------------------
# Employee retrieval helpers
# ---------------------------------------------------------------------------

def _find_employee_by_name(name: str):
    """Fetch employee record by name via the REST API."""
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/employee/{name}",
            timeout=5,
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if "error" in data:
            return None
        return data
    except Exception as e:
        print(f"[Retrieval Agent] Employee API error: {e}")
        return None


# ---------------------------------------------------------------------------
# Team / hierarchy helpers
# ---------------------------------------------------------------------------

def _get_direct_reports(manager_id):
    db = SessionLocal()
    try:
        return db.query(Employee).filter(Employee.manager_id == manager_id).all()
    finally:
        db.close()


def _build_tree_recursive(manager_id, level=0):
    reports = _get_direct_reports(manager_id)
    tree_str = ""
    for r in reports:
        indent = "│   " * level
        tree_str += f"{indent}├── {r.name} ({r.designation})\n"
        tree_str += _build_tree_recursive(r.employee_id, level + 1)
    return tree_str


def _resolve_team_data(state: Dict[str, Any], trace: list):
    """
    Build team / hierarchy data when team_lookup, org_analytics, or
    department_info intents are present.
    Returns a team_data dict or None.
    """
    intents = state.get("intents", [])
    if not any(i in intents for i in ["team_lookup", "org_analytics", "org_chart", "department_info"]):
        return None

    employee_name = state.get("employee_name")
    department_name = state.get("department_name")
    current_user = state.get("current_user")

    db = SessionLocal()
    try:
        target_employee = None

        # Priority 1: specific employee named in query
        if employee_name:
            target_employee = (
                db.query(Employee)
                .filter(Employee.name.ilike(f"%{employee_name}%"))
                .first()
            )

        # Priority 2: department head (when dept_info requested)
        if not target_employee and department_name:
            target_employee = (
                db.query(Employee)
                .filter(
                    Employee.department.ilike(f"{department_name}"),
                    Employee.role.in_(["DEPT_DIRECTOR", "HR_HEAD", "CEO"]),
                )
                .order_by(Employee.salary.desc())
                .first()
            )
            if target_employee:
                trace.append(
                    f"Retrieval Agent → Resolved hierarchy root to dept head: {target_employee.name}"
                )

        # Priority 3: current user (fallback for team_lookup)
        if not target_employee and current_user:
            target_employee = (
                db.query(Employee)
                .filter(Employee.employee_id == current_user["employee_id"])
                .first()
            )

        if not target_employee:
            trace.append("Retrieval Agent → No suitable target found for hierarchy building.")
            return None

        trace.append(f"Retrieval Agent → Building recursive hierarchy from {target_employee.name}")

        full_tree = f"{target_employee.name} ({target_employee.designation})\n"
        full_tree += _build_tree_recursive(target_employee.employee_id)

        reports = _get_direct_reports(target_employee.employee_id)
        return {
            "full_hierarchy": full_tree,
            "direct_reports": [
                {"name": r.name, "role": r.role, "designation": r.designation}
                for r in reports
            ],
        }
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Main agent function
# ---------------------------------------------------------------------------

def retrieval_agent(state: Dict[str, Any]):
    """
    Single retrieval agent — replaces team_lookup_agent, employee_lookup_agent,
    and department_agent.  No LLM calls are made here.
    """
    intents = state.get("intents", [])
    trace = state.get("trace", [])
    updates: Dict[str, Any] = {"trace": trace}

    print("\n========== RETRIEVAL AGENT ==========")
    print("intents =", intents)
    print("employee_name =", state.get("employee_name"))
    print("department_name =", state.get("department_name"))
    print("=====================================")

    # ------------------------------------------------------------------
    # 1. Organization-wide analytics
    # ------------------------------------------------------------------
    if "org_analytics" in intents:
        trace.append("Retrieval Agent → Fetching comprehensive organization-wide analytics")
        updates["organization_data"] = {
            "department_stats": get_all_department_stats(),
            "overall_stats": get_organization_stats(),
            "heads": get_department_heads(),
            "top_paid_employees": get_top_paid_employees(10),
        }

    # ------------------------------------------------------------------
    # 2. Promotion analysis
    # ------------------------------------------------------------------
    if "promotion_analysis" in intents:
        dept_name = state.get("department_name")
        trace.append(
            f"Retrieval Agent → Identifying promotion candidates"
            + (f" for {dept_name}" if dept_name else "")
        )
        candidates = get_promotion_candidates(dept_name)
        print(f"[DEBUG] Promotion Candidates for {dept_name}: {candidates}")
        updates["promotion_candidates"] = candidates

    # ------------------------------------------------------------------
    # 3. Team / hierarchy lookup
    # ------------------------------------------------------------------
    team_data = _resolve_team_data(state, trace)
    if team_data is not None:
        updates["team_data"] = team_data

    # ------------------------------------------------------------------
    # 4. Employee lookup + manager resolution
    # ------------------------------------------------------------------
    employee_name = state.get("employee_name")
    if employee_name:
        employee = _find_employee_by_name(employee_name)
        if employee:
            manager_id = employee.get("manager_id")
            manager_info = get_manager_data(manager_id)
            employee["manager_data"] = manager_info
            employee["manager_name"] = manager_info["name"] if manager_info else "None"
            employee["manager_designation"] = manager_info["designation"] if manager_info else "N/A"

            current_user = state.get("current_user")
            role = current_user["role"]
            employee = filter_employee(employee, role)

            trace.append(
                f"Retrieval Agent → Retrieved data for {employee_name}"
                f" (Managed by: {employee['manager_name']})"
            )
        else:
            trace.append(f"Retrieval Agent → No profile found for '{employee_name}'")
        updates["employee_data"] = employee

    # ------------------------------------------------------------------
    # 5. Department statistics
    # ------------------------------------------------------------------
    dept_name = state.get("department_name")
    if not dept_name and updates.get("employee_data"):
        dept_name = updates["employee_data"].get("department")

    if dept_name and "org_analytics" not in intents:
        stats = get_department_stats(dept_name)
        trace.append(
            f"Retrieval Agent → Compiled analytics for {dept_name}"
            f" (Avg Salary: ${stats['average_salary']})"
        )
        updates["department_stats"] = stats

    return updates
