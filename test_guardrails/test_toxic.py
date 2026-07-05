from guardrails.hub import ToxicLanguage
from guardrails import OnFailAction

print("Creating ToxicLanguage validator...")

validator = ToxicLanguage(
    threshold=0.8,
    validation_method="sentence",
    on_fail=OnFailAction.EXCEPTION
)

print("Validator created successfully!")
print(type(validator))