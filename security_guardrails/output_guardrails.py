import re

from security_guardrails.audit_logger import log_guardrail_event


EMAIL_PATTERN = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

PASSWORD_PATTERNS = [
    r"password\s*:",
    r"password\s*=",
    r"ceo123",
    r"manager123",
    r"employee123"
]


def validate_output(
    response: str,
    current_user: dict
):

    # Email leakage detection
    if re.search(EMAIL_PATTERN, response):

        log_guardrail_event(
            current_user["name"],
            current_user["role"],
            response[:100],
            "BLOCKED",
            "Email Leakage"
        )

        response = re.sub(
            EMAIL_PATTERN,
            "[REDACTED_EMAIL]",
            response
        )
        return{
            "allowed": True,
            "response": response,
        }

    # Password leakage detection
    for pattern in PASSWORD_PATTERNS:

        if re.search(pattern, response.lower()):

            log_guardrail_event(
                current_user["name"],
                current_user["role"],
                response[:100],
                "BLOCKED",
                "Password Leakage"
            )

            return {
                "allowed": False,
                "reason": "Password Leakage"
            }

    return {
        "allowed": True
    }