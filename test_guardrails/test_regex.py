from guardrails.hub import RegexMatch
from guardrails import OnFailAction

print("Creating Regex validator...")

validator = RegexMatch(
    regex=r"^[A-Za-z ]+$",
    on_fail=OnFailAction.EXCEPTION
)

print("Validator created successfully!")
print(type(validator))