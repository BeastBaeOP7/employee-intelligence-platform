from guardrails.validator_base import (
    Validator,
    register_validator,
    PassResult,
    FailResult,
)


@register_validator(
    name="enterprise/role_escalation",
    data_type="string",
)
class RoleEscalationValidator(Validator):

    PATTERNS = [
        "act as ceo",
        "pretend you are ceo",
        "assume ceo",
        "i am ceo",
        "ignore rbac",
        "become administrator",
        "act as admin",
    ]

    def validate(self, value, metadata):

        query = value.lower()

        for pattern in self.PATTERNS:

            if pattern in query:

                return FailResult(
                    error_message=f"Role Escalation detected: {pattern}"
                )

        return PassResult()