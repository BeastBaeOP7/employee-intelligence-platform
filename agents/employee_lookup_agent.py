from tools.employee_search_tool import find_employee_by_name
from utils.employee_utils import get_manager_data

def employee_lookup_agent(state):
    employee_name = state.get("employee_name")
    trace = state.get("trace", [])
    
    if not employee_name:
        return state

    employee = find_employee_by_name(employee_name)
    
    if employee:
        # Resolve manager data
        manager_id = employee.get("manager_id")
        manager_info = get_manager_data(manager_id)
        employee["manager_data"] = manager_info
        employee["manager_name"] = manager_info["name"] if manager_info else "None"
        employee["manager_designation"] = manager_info["designation"] if manager_info else "N/A"
        
        trace.append(f"Employee Lookup Agent → Retrieved data for {employee_name} (Managed by: {employee['manager_name']})")
    else:
        trace.append(f"Employee Lookup Agent → No profile found for '{employee_name}'")

    return {
        "employee_data": employee,
        "trace": trace
    }