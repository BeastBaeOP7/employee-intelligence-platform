from fastapi import FastAPI
from database.database import SessionLocal
from database.models import Employee

app = FastAPI(
    title="Employee Service API"
)


@app.get("/employee/{name}")
def get_employee(name: str):
    print(f"API called with name: {name}")

    db = SessionLocal()

    employee = (
        db.query(Employee)
        .filter(Employee.name.ilike(f"%{name}%"))
        .first()
    )

    db.close()

    if not employee:
        return {
            "error": "Employee not found"
        }

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
        "join_date": employee.join_date
    }