from security_guardrails.engine import engine

text = """
Employee Name: Ryan Cooper
Email: ryan.cooper@company.com
Phone: 9876543210
Credit Card: 4111 1111 1111 1111
IP Address: 192.168.1.10
Website: https://company.com
Location: San Francisco
"""

result = engine.validate_output(text)

print("========== ORIGINAL ==========")
print(text)

print("\n========== AFTER GUARDRAILS ==========")
print(result["response"])