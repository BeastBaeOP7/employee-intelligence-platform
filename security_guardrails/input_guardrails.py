import re

from security_guardrails.audit_logger import log_guardrail_event
from security_guardrails.guardrails_engine import validate_with_guardrails_ai

PROMPT_INJECTION_PATTERNS = [
    r"ignore.*instruction",
    r"forget.*rule",
    r"reveal.*prompt",
    r"show.*system.*prompt",
    r"act as.*administrator",
    r"act as.*ceo",
    r"bypass.*security",
    r"override.*restriction"
]

ROLE_ESCALATION_PATTERNS = [
    r"pretend.*ceo",
    r"assume.*ceo",
    r"i am.*ceo",
    r"ignore.*rbac"
]

SQL_PATTERNS = [
    r"or\s+1=1",
    r"drop\s+table",
    r"union\s+select",
    r"delete\s+from",
    r"insert\s+into"
]

OFF_DOMAIN_PATTERNS = [
    r"ipl",
    r"fifa",
    r"world cup",
    r"weather",
    r"movie",
    r"python code",
    r"react code",
    r"javascript code"
]

SENSITIVE_DATA_PATTERNS = [
    r"password",
    r"login password",
    r"show passwords",
    r"reveal passwords",
    r"employee passwords",
    r"credentials",
    r"login credentials",
    r"api key",
    r"secret key",
    r"token"
]

def validate_input(query: str, current_user: dict):
    ai_result = validate_with_guardrails_ai(query)

    if not ai_result["allowed"]:
        return ai_result

    query_lower = query.lower()

    checks = {
        "Prompt Injection": PROMPT_INJECTION_PATTERNS,
        "Role Escalation": ROLE_ESCALATION_PATTERNS,
        "SQL Injection": SQL_PATTERNS,
        "Sensitive Data Access": SENSITIVE_DATA_PATTERNS,
        "Off Domain": OFF_DOMAIN_PATTERNS
    }

    for reason, patterns in checks.items():

        for pattern in patterns:

            if re.search(pattern, query_lower):

                log_guardrail_event(
                    current_user["name"],
                    current_user["role"],
                    query,
                    "BLOCKED",
                    reason
                )

                return {
                    "allowed": False,
                    "reason": reason
                }

    log_guardrail_event(
        current_user["name"],
        current_user["role"],
        query,
        "ALLOWED",
        "Passed Input Guardrails"
    )

    return {
        "allowed": True
    }