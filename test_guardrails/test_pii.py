from guardrails.hub import GuardrailsPII

validator = GuardrailsPII(
    entities="pii",
    use_local=True
)

tests = [
    "Ryan Cooper",
    "admin@gmail.com",
    "Phone: 9876543210",
    "Ryan Cooper admin@gmail.com"
]

for t in tests:
    print("=" * 50)
    print(t)
    print(validator.validate(t, {}))