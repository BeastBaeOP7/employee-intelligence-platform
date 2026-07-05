from validator import RestrictToTopic

validator = RestrictToTopic(
    valid_topics=[
        "Employee Profiles",
        "Salary Analytics",
        "Department Analytics"
    ],
    disable_classifier=False,
    disable_llm=True
)

print(validator.validate("Who manages Ryan Cooper?", {}))
print(validator.validate("Who won IPL 2026?", {}))