from sqlalchemy import func

from database.database import SessionLocal
from database.models import Employee


def get_department_stats(department: str):
    db = SessionLocal()
    try:
        avg_salary = db.query(func.avg(Employee.salary)).filter(Employee.department == department).scalar()
        max_salary = db.query(func.max(Employee.salary)).filter(Employee.department == department).scalar()
        min_salary = db.query(func.min(Employee.salary)).filter(Employee.department == department).scalar()
        count = db.query(Employee).filter(Employee.department == department).count()
        avg_perf = db.query(func.avg(Employee.performance_rating)).filter(Employee.department == department).scalar()
        
        # Department Head
        head = db.query(Employee).filter(
            Employee.department == department,
            Employee.role.in_(['DEPT_DIRECTOR', 'HR_HEAD', 'CEO'])
        ).first()

        # Managers
        managers = db.query(Employee).filter(
            Employee.department == department,
            Employee.role == 'MANAGER'
        ).all()

        # Employees
        employees = db.query(Employee).filter(
            Employee.department == department
        ).all()

        return {
            "department_name": department,
            "department_head": head.name if head else "N/A",
            "manager_count": len(managers),
            "managers": [m.name for m in managers],
            "employee_count": count,
            "employees": [e.name for e in employees],
            "average_salary": round(avg_salary or 0, 2),
            "highest_salary": max_salary or 0,
            "lowest_salary": min_salary or 0,
            "average_performance_rating": round(avg_perf or 0, 2)
        }
    finally:
        db.close()


def get_organization_stats():
    db = SessionLocal()
    try:
        total_employees = db.query(Employee).count()
        avg_salary = db.query(func.avg(Employee.salary)).scalar()
        max_salary = db.query(func.max(Employee.salary)).scalar()
        
        # Dept with highest avg salary
        dept_salaries = db.query(
            Employee.department, 
            func.avg(Employee.salary).label('avg_salary')
        ).group_by(Employee.department).all()
        highest_paid_dept = max(dept_salaries, key=lambda x: x[1])[0] if dept_salaries else "N/A"

        # Dept with most employees
        dept_counts = db.query(
            Employee.department, 
            func.count(Employee.employee_id).label('count')
        ).group_by(Employee.department).all()
        largest_dept = max(dept_counts, key=lambda x: x[1])[0] if dept_counts else "N/A"

        # Dept with highest performance
        dept_perf = db.query(
            Employee.department, 
            func.avg(Employee.performance_rating).label('avg_perf')
        ).group_by(Employee.department).all()
        top_perf_dept = max(dept_perf, key=lambda x: x[1])[0] if dept_perf else "N/A"

        return {
            "total_employees": total_employees,
            "avg_salary": round(avg_salary or 0, 2),
            "max_salary": max_salary or 0,
            "highest_paid_department": highest_paid_dept,
            "largest_department": largest_dept,
            "top_performing_department": top_perf_dept
        }
    finally:
        db.close()

def get_all_department_stats():
    """Returns analytics for every department."""
    db = SessionLocal()
    try:
        results = db.query(
            Employee.department,
            func.count(Employee.employee_id).label('count'),
            func.avg(Employee.salary).label('avg_salary'),
            func.max(Employee.salary).label('max_salary'),
            func.avg(Employee.performance_rating).label('avg_rating')
        ).group_by(Employee.department).all()
        
        return [
            {
                "department": r.department,
                "employee_count": r.count,
                "average_salary": round(r.avg_salary or 0, 2),
                "highest_salary": r.max_salary or 0,
                "average_performance_rating": round(r.avg_rating or 0, 2)
            }
            for r in results
        ]
    finally:
        db.close()

def get_promotion_candidates(department: str = None):
    """Returns ranked promotion candidates based on rating >= 4.5 and exp >= 5."""
    db = SessionLocal()
    try:
        query = db.query(Employee).filter(
            Employee.performance_rating >= 4.5,
            Employee.experience_years >= 5
        )
        
        if department:
            query = query.filter(Employee.department.ilike(f"{department}"))
            
        candidates = query.order_by(
            Employee.performance_rating.desc(), 
            Employee.experience_years.desc(),
            Employee.salary.asc()
        ).all()
        
        return [
            {
                "name": c.name,
                "department": c.department,
                "designation": c.designation,
                "performance_rating": c.performance_rating,
                "experience_years": c.experience_years,
                "salary": c.salary
            }
            for c in candidates
        ]
    finally:
        db.close()

def get_top_paid_employees(n=10):
    db = SessionLocal()
    try:
        top_employees = db.query(Employee).order_by(Employee.salary.desc()).limit(n).all()
        return [
            {"name": e.name, "salary": e.salary, "department": e.department, "designation": e.designation}
            for e in top_employees
        ]
    finally:
        db.close()


def get_department_heads():
    db = SessionLocal()
    try:
        # Precise mapping as per requirement
        depts = ["HR", "IT", "Sales", "Marketing", "Product", "Executive"]
        heads = []
        for d in depts:
            role_filter = ['DEPT_DIRECTOR', 'HR_HEAD', 'CEO']
            if d == "Product":
                 role_filter.append('MANAGER') # Kevin Malone is MANAGER in seed but Head of Product
            
            head = db.query(Employee).filter(
                Employee.department == d,
                Employee.role.in_(role_filter)
            ).order_by(Employee.salary.desc()).first() # Take the highest ranking person in that dept
            
            if head:
                heads.append({"department": d, "name": head.name, "designation": head.designation})
            elif d == "Executive":
                # Special Case: CEO might be in Executive
                head = db.query(Employee).filter(Employee.role == 'CEO').first()
                if head:
                    heads.append({"department": "CEO", "name": head.name, "designation": head.designation})

        return heads
    finally:
        db.close()