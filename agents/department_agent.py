from tools.department_api_tool import (
    get_department_stats,
    get_organization_stats,
    get_department_heads,
    get_all_department_stats,
    get_promotion_candidates,
    get_top_paid_employees
)


def department_agent(state):
    intents = state.get("intents", [])
    trace = state.get("trace", [])
    
    # Handle Organization-Wide Analytics
    if "org_analytics" in intents:
        trace.append("Department Agent → Fetching comprehensive organization-wide analytics")
        all_dept_stats = get_all_department_stats()
        org_stats = get_organization_stats()
        dept_heads = get_department_heads()
        top_paid = get_top_paid_employees(10)
        
        return {
            "organization_data": {
                "department_stats": all_dept_stats,
                "overall_stats": org_stats,
                "heads": dept_heads,
                "top_paid_employees": top_paid
            },
            "trace": trace
        }

    # Handle Promotion Analysis
    if "promotion_analysis" in intents:
        trace.append("Department Agent → Identifying top promotion candidates based on business rules")
        candidates = get_promotion_candidates()
        return {
            "promotion_candidates": candidates,
            "trace": trace
        }


    dept_name = state.get("department_name")
    employee = state.get("employee_data")

    if not dept_name and employee:
        dept_name = employee.get("department")

    if not dept_name:
        trace.append("Department Agent → No specific department context found. Skipping departmental analytics.")
        return {
            "department_stats": None,
            "trace": trace
        }

    stats = get_department_stats(dept_name)
    trace.append(f"Department Agent → Compiled analytics for {dept_name} (Avg Salary: ${stats['average_salary']})")

    return {
        "department_stats": stats,
        "trace": trace
    }