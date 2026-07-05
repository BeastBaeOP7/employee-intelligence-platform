from guardrails.hub import GuardrailsPII

validator = GuardrailsPII(
    entities="pii",
    use_local=True
)

text = """
Ryan Cooper
Email: ryan.cooper@company.com
Phone: 9876543210
"""

anonymized, spans = validator.anonymize(
    text,
    validator.entities
)

print("ANONYMIZED:")
print(anonymized)

print("\nERROR SPANS:")
print(spans)