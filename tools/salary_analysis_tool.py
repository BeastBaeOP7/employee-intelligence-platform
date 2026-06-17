def compare_salary(employee_data, department_stats):

    employee_salary = employee_data["salary"]
    average_salary = department_stats["average_salary"]

    difference = employee_salary - average_salary

    return {
        "employee_salary": employee_salary,
        "department_average": average_salary,
        "difference": difference,
        "above_average": difference > 0
    }