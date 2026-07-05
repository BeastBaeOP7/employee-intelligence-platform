from guardrails import Guard
from guardrails import OnFailAction

from guardrails.hub import RegexMatch

print("Creating Guard...")

guard = Guard()

guard.use(
    RegexMatch(
        regex=r"^[A-Za-z ]+$",
        on_fail=OnFailAction.EXCEPTION
    )
)

print("Guard created successfully!")

print()

print("Testing valid input...")

result = guard.validate("Ryan Cooper")

print(result)

print()

print("Testing invalid input...")

try:

    result = guard.validate("DROP TABLE employees")

    print(result)

except Exception as e:

    print(type(e))
    print(e)