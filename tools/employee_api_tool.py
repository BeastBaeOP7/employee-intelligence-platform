from database.database import SessionLocal
from database.models import Employee


def get_employee(employee_id: int):
    db = SessionLocal()

    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    db.close()

    if not employee:
        return None

    return {
        "employee_id": employee.employee_id,
        "name": employee.name,
        "department": employee.department,
        "designation": employee.designation,
        "salary": employee.salary,
        "experience_years": employee.experience_years
    }