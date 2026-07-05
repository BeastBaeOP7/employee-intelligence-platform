from security_guardrails.engine import engine


def validate_input(query, current_user):

    return engine.validate_input(query)