from database.database import SessionLocal
from database.models import Employee

def get_manager_data(manager_id):
    if not manager_id:
        return None
    
    db = SessionLocal()
    try:
        manager = db.query(Employee).filter(Employee.employee_id == manager_id).first()
        if manager:
            return {
                "name": manager.name,
                "designation": manager.designation,
                "role": manager.role,
                "department": manager.department
            }
        return None
    finally:
        db.close()


def get_employee_by_id(employee_id):
    db = SessionLocal()
    try:
        return db.query(Employee).filter(Employee.employee_id == employee_id).first()
    finally:
        db.close()
