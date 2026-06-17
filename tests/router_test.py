from agents.controller_agent import controller_agent

result = controller_agent(
    {
        "user_query": "Is John Doe paid above average?"
    }
)

print("\nFINAL RESULT:")
print(result)