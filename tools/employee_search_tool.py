from database.database import SessionLocal
from database.models import Employee


def find_employee_by_name(name: str):
    db = SessionLocal()
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.name.ilike(f"%{name}%"))
            .first()
        )
        if not employee:
            return None
        return {
            "employee_id": employee.employee_id,
            "name": employee.name,
            "email": employee.email,
            "department": employee.department,
            "designation": employee.designation,
            "role": employee.role,
            "salary": employee.salary,
            "experience_years": employee.experience_years,
            "manager_id": employee.manager_id,
            "location": employee.location,
            "performance_rating": employee.performance_rating,
            "join_date": employee.join_date,
            "credit_card": employee.credit_card,
        }
    except Exception as e:
        print("DB ERROR:", e)
        return None
    finally:
        db.close()