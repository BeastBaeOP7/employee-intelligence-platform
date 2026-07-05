from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_login = Column(String, nullable=True)
    department = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    role = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)
    experience_years = Column(Integer, nullable=False)
    manager_id = Column(Integer, nullable=True)
    location = Column(String, nullable=False)
    performance_rating = Column(Float, nullable=False)
    join_date = Column(String, nullable=False)
    credit_card = Column(String(20), nullable=True)

