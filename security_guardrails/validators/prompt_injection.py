from guardrails.validator_base import (
    Validator,
    register_validator,
    PassResult,
    FailResult,
)


@register_validator(
    name="enterprise/prompt_injection",
    data_type="string",
)
class PromptInjectionValidator(Validator):

    PATTERNS = [
        "ignore previous instructions",
        "ignore all instructions",
        "forget previous instructions",
        "reveal system prompt",
        "show system prompt",
        "developer instructions",
        "bypass security",
        "override restrictions",
        "jailbreak",
    ]

    def validate(self, value, metadata):

        query = value.lower()

        for pattern in self.PATTERNS:

            if pattern in query:

                return FailResult(
                    error_message=f"Prompt Injection detected: {pattern}"
                )

        return PassResult()