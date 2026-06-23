from database.database import engine, SessionLocal
from database.models import Base, Employee

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

db = SessionLocal()

employees = [
    # Executive
    Employee(employee_id=1, name="Mike Miller", email="ceo@company.com", password="ceo123", department="Executive", designation="CEO", role="CEO", salary=500000, experience_years=20, manager_id=None, location="New York", performance_rating=5.0, join_date="2010-01-01"),

    # HR
    Employee(employee_id=2, name="Linda Green", email="linda.green@company.com",password="ceo123", department="HR", designation="HR Head", role="HR_HEAD", salary=200000, experience_years=15, manager_id=1, location="Chicago", performance_rating=4.8, join_date="2012-05-15"),
    Employee(employee_id=3, name="Sarah Smith", email="sarah.smith@company.com",password="manager123", department="HR", designation="HR Manager", role="MANAGER", salary=120000, experience_years=10, manager_id=2, location="Chicago", performance_rating=4.5, join_date="2015-08-20"),
    Employee(employee_id=4, name="John Doe", email="john.doe@company.com",password="employee123", department="HR", designation="HR Specialist", role="EMPLOYEE", salary=70000, experience_years=5, manager_id=3, location="Chicago", performance_rating=4.2, join_date="2018-03-10"),
    Employee(employee_id=5, name="Jane Smith", email="jane.smith@company.com",password="employee123", department="HR", designation="HR Assistant", role="EMPLOYEE", salary=55000, experience_years=2, manager_id=3, location="Chicago", performance_rating=4.0, join_date="2021-11-12"),
    Employee(employee_id=6, name="Alice Brown", email="alice.brown@company.com",password="manager123", department="HR", designation="HR Lead", role="MANAGER", salary=115000, experience_years=9, manager_id=2, location="Chicago", performance_rating=4.4, join_date="2016-02-14"),
    Employee(employee_id=7, name="Bob White", email="bob.white@company.com",password="employee123", department="HR", designation="Recruiter", role="EMPLOYEE", salary=65000, experience_years=4, manager_id=6, location="Chicago", performance_rating=4.1, join_date="2019-07-01"),
    Employee(employee_id=26, name="Emily Davis", email="emily.davis@company.com",password="employee123", department="HR", designation="HR Coordinator", role="EMPLOYEE", salary=62000, experience_years=3, manager_id=3, location="Chicago", performance_rating=4.1, join_date="2022-02-15"),
    Employee(employee_id=27, name="Robert Walker", email="robert.walker@company.com",password="employee123", department="HR", designation="Talent Acquisition Specialist", role="EMPLOYEE", salary=68000, experience_years=5, manager_id=3, location="Chicago", performance_rating=4.3, join_date="2020-07-11"),
    Employee(employee_id=28, name="Sophia Turner", email="sophia.turner@company.com",password="employee123", department="HR", designation="Recruitment Specialist", role="EMPLOYEE", salary=66000, experience_years=4, manager_id=6, location="Chicago", performance_rating=4.2, join_date="2021-06-21"),
    Employee(employee_id=29, name="Liam Foster", email="liam.foster@company.com",password="employee123", department="HR", designation="HR Analyst", role="EMPLOYEE", salary=70000, experience_years=5, manager_id=6, location="Chicago", performance_rating=4.4, join_date="2019-10-01"),

    # IT
    Employee(employee_id=8, name="Alex Johnson", email="alex.johnson@company.com",password="manager123", department="IT", designation="IT Director", role="DEPT_DIRECTOR", salary=220000, experience_years=18, manager_id=1, location="San Francisco", performance_rating=4.9, join_date="2011-06-30"),
    Employee(employee_id=9, name="Mark Tech", email="mark.tech@company.com",password="manager123", department="IT", designation="Software Engineering Manager", role="MANAGER", salary=150000, experience_years=12, manager_id=8, location="San Francisco", performance_rating=4.7, join_date="2014-04-10"),
    Employee(employee_id=10, name="Ryan Cooper", email="ryan.cooper@company.com",password="employee123", department="IT", designation="Senior Developer", role="EMPLOYEE", salary=110000, experience_years=7, manager_id=9, location="San Francisco", performance_rating=4.5, join_date="2017-09-15"),
    Employee(employee_id=11, name="Daniel Kim", email="daniel.kim@company.com",password="employee123", department="IT", designation="Junior Developer", role="EMPLOYEE", salary=80000, experience_years=2, manager_id=9, location="San Francisco", performance_rating=4.3, join_date="2022-01-20"),
    Employee(employee_id=12, name="Sam Sysadmin", email="sam.sys@company.com",password="manager123", department="IT", designation="IT Infrastructure Manager", role="MANAGER", salary=140000, experience_years=11, manager_id=8, location="San Francisco", performance_rating=4.6, join_date="2015-11-05"),
    Employee(employee_id=13, name="Emma Wilson", email="emma.wilson@company.com",password="employee123", department="IT", designation="DevOps Engineer", role="EMPLOYEE", salary=115000, experience_years=6, manager_id=12, location="San Francisco", performance_rating=4.4, join_date="2018-05-22"),
    Employee(employee_id=30, name="Jason Miller", email="jason.miller@company.com",password="employee123", department="IT", designation="Backend Developer", role="EMPLOYEE", salary=105000, experience_years=6, manager_id=9, location="San Francisco", performance_rating=4.4, join_date="2019-05-10"),
    Employee(employee_id=31, name="Chloe Adams", email="chloe.adams@company.com",password="employee123", department="IT", designation="Frontend Developer", role="EMPLOYEE", salary=98000, experience_years=4, manager_id=9, location="San Francisco", performance_rating=4.2, join_date="2021-03-15"),
    Employee(employee_id=32, name="Noah Bennett", email="noah.bennett@company.com",password="employee123", department="IT", designation="Cloud Engineer", role="EMPLOYEE", salary=118000, experience_years=7, manager_id=12, location="San Francisco", performance_rating=4.6, join_date="2018-08-10"),
    Employee(employee_id=33, name="Grace Parker", email="grace.parker@company.com",password="employee123", department="IT", designation="Site Reliability Engineer", role="EMPLOYEE", salary=120000, experience_years=6, manager_id=12, location="San Francisco", performance_rating=4.5, join_date="2019-02-11"),

    # Sales
    Employee(employee_id=14, name="David Brown", email="david.brown@company.com",password="manager123", department="Sales", designation="Sales Director", role="DEPT_DIRECTOR", salary=210000, experience_years=17, manager_id=1, location="Dallas", performance_rating=4.8, join_date="2012-08-12"),
    Employee(employee_id=15, name="David Harris", email="david.harris@company.com",password="manager123", department="Sales", designation="Sales Manager", role="MANAGER", salary=140000, experience_years=10, manager_id=14, location="Dallas", performance_rating=4.5, join_date="2016-03-18"),
    Employee(employee_id=16, name="Jim Halpert", email="jim.halpert@company.com",password="employee123", department="Sales", designation="Sales Executive", role="EMPLOYEE", salary=75000, experience_years=3, manager_id=15, location="Dallas", performance_rating=4.2, join_date="2021-02-10"),
    Employee(employee_id=17, name="Emily Clark", email="emily.clark@company.com",password="manager123", department="Sales", designation="Account Manager", role="MANAGER", salary=135000, experience_years=9, manager_id=14, location="Dallas", performance_rating=4.4, join_date="2017-10-05"),
    Employee(employee_id=18, name="Dwight Schrute", email="dwight.schrute@company.com",password="employee123", department="Sales", designation="Senior Sales Executive", role="EMPLOYEE", salary=72000, experience_years=4, manager_id=17, location="Dallas", performance_rating=4.1, join_date="2020-05-30"),
    Employee(employee_id=34, name="Michael Reed", email="michael.reed@company.com",password="employee123", department="Sales", designation="Sales Executive", role="EMPLOYEE", salary=78000, experience_years=4, manager_id=15, location="Dallas", performance_rating=4.3, join_date="2020-09-14"),
    Employee(employee_id=35, name="Ethan Clark", email="ethan.clark@company.com",password="employee123", department="Sales", designation="Business Development Executive", role="EMPLOYEE", salary=82000, experience_years=5, manager_id=15, location="Dallas", performance_rating=4.5, join_date="2019-11-02"),
    Employee(employee_id=36, name="Lucas Green", email="lucas.green@company.com",password="employee123", department="Sales", designation="Sales Executive", role="EMPLOYEE", salary=76000, experience_years=3, manager_id=17, location="Dallas", performance_rating=4.1, join_date="2021-08-18"),
    Employee(employee_id=37, name="Olivia King", email="olivia.king@company.com",password="employee123", department="Sales", designation="Account Executive", role="EMPLOYEE", salary=85000, experience_years=6, manager_id=17, location="Dallas", performance_rating=4.6, join_date="2018-12-07"),

    # Marketing
    Employee(employee_id=20, name="Sophia White", email="sophia.white@company.com",password="manager123", department="Marketing", designation="Marketing Director", role="DEPT_DIRECTOR", salary=205000, experience_years=16, manager_id=1, location="Los Angeles", performance_rating=4.7, join_date="2013-02-10"),
    Employee(employee_id=22, name="Ryan Gosling", email="ryan.g@company.com",password="manager123", department="Marketing", designation="Marketing Manager", role="MANAGER", salary=130000, experience_years=10, manager_id=20, location="Los Angeles", performance_rating=4.4, join_date="2017-06-15"),
    Employee(employee_id=38, name="Rachel Adams", email="rachel.adams@company.com",password="employee123", department="Marketing", designation="Content Strategist", role="EMPLOYEE", salary=72000, experience_years=5, manager_id=20, location="Los Angeles", performance_rating=4.3, join_date="2020-01-12"),
    Employee(employee_id=39, name="Aaron Lewis", email="aaron.lewis@company.com",password="employee123", department="Marketing", designation="SEO Specialist", role="EMPLOYEE", salary=75000, experience_years=6, manager_id=20, location="Los Angeles", performance_rating=4.5, join_date="2019-04-25"),
    Employee(employee_id=40, name="Emma Davis", email="emma.d@company.com",password="employee123", department="Marketing", designation="Brand Specialist", role="EMPLOYEE", salary=70000, experience_years=4, manager_id=22, location="Los Angeles", performance_rating=4.2, join_date="2021-05-15"),
    Employee(employee_id=41, name="Jacob Turner", email="jacob.t@company.com",password="employee123", department="Marketing", designation="Digital Marketing Specialist", role="EMPLOYEE", salary=77000, experience_years=5, manager_id=22, location="Los Angeles", performance_rating=4.4, join_date="2020-07-08"),

    # Product
    Employee(employee_id=24, name="Kevin Malone", email="kevin.malone@company.com",password="manager123", department="Product", designation="Product Manager", role="MANAGER", salary=160000, experience_years=12, manager_id=1, location="New York", performance_rating=4.6, join_date="2014-08-20"),
    Employee(employee_id=46, name="Ethan Cooper", email="ethan.cooper@company.com",password="employee123", department="Product", designation="Product Analyst", role="EMPLOYEE", salary=95000, experience_years=4, manager_id=24, location="New York", performance_rating=4.4, join_date="2021-01-20"),
    Employee(employee_id=47, name="Chloe Walker", email="chloe.walker@company.com",password="employee123", department="Product", designation="UX Designer", role="EMPLOYEE", salary=92000, experience_years=5, manager_id=24, location="New York", performance_rating=4.3, join_date="2020-03-15"),
    Employee(employee_id=48, name="Isabella Reed", email="isabella.reed@company.com",password="employee123", department="Product", designation="Associate Product Manager", role="EMPLOYEE", salary=98000, experience_years=6, manager_id=24, location="New York", performance_rating=4.6, join_date="2019-06-12"),
    Employee(employee_id=49, name="Nathan Scott", email="nathan.scott@company.com",password="employee123", department="Product", designation="Product Designer", role="EMPLOYEE", salary=90000, experience_years=4, manager_id=24, location="New York", performance_rating=4.2, join_date="2021-09-01"),
]

db.add_all(employees)
db.commit()
db.close()

print("Database seeded successfully with 44 employees.")
