from security_guardrails.validators.sql_injection import SQLInjectionValidator

validator = SQLInjectionValidator()

tests = [
    "Who manages Ryan Cooper?",
    "DROP TABLE employees",
    "DELETE FROM employees",
    "UNION SELECT * FROM users",
]

for test in tests:

    result = validator.validate(test, {})

    print(test)

    print(result)

    print("-" * 50)