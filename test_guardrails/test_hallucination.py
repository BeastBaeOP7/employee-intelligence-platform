from guardrails_grhub_provenance_llm import ProvenanceLLM
from config.github_models_llm import get_llm

llm = get_llm()

def github_llm(prompt):
    return llm.invoke(prompt).content

validator = ProvenanceLLM(
    validation_method="sentence",
    llm_callable=github_llm
)

context = """
Ryan Cooper is a Senior Developer in the IT department.
His salary is $110,000.
He has 7 years of experience.
His manager is Mark Tech.
"""

good_response = """
Ryan Cooper is a Senior Developer in the IT department and reports to Mark Tech.
"""

bad_response = """
Ryan Cooper is a Senior Developer.
His blood group is O+.
He graduated from Stanford University.
"""

metadata = {
    "sources": [context]
}

print("===== GOOD RESPONSE =====")
result = validator.validate(
    good_response,
    metadata
)

print(result)

print("\n===== BAD RESPONSE =====")
result = validator.validate(
    bad_response,
    metadata
)

print(result)