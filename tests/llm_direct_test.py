from config.github_models_llm import get_llm

llm = get_llm()

print("Testing LLM...")

response = llm.invoke(
    "Reply with exactly: HELLO"
)

print(response.content)