from security_guardrails.engine import engine

# FIX: Accept current_user so ExportPolicyValidator can enforce role-based export rules.
def validate_output(response, context, current_user=None):

    result = engine.validate_output(response, context, current_user=current_user)

    if result["allowed"]:
        return {
            "allowed": True,
            "response": result.get("response", response)  # use masked text from engine
        }

    return {
        "allowed": False,
        "reason": result["reason"],
        "response": result.get("response", response)
    }