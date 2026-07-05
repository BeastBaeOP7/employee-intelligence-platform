from security_guardrails.engine import engine

def validate_output(response, context):

    result = engine.validate_output(response, context)

    if result["allowed"]:
        return {
            "allowed": True,
            "response": response
        }

    return {
        "allowed": False,
        "reason": result["reason"],
        "response": result.get("response", response)
    }