from guardrails.validator_base import (
    Validator,
    register_validator,
    PassResult,
    FailResult,
)


@register_validator(
    name="enterprise/off_domain",
    data_type="string",
)
class OffDomainValidator(Validator):

    BLOCKED = [
        "ipl",
        "cricket",
        "football",
        "weather",
        "movie",
        "netflix",
        "python code",
        "javascript",
        "react",
    ]

    def validate(self, value, metadata):

        query = value.lower()

        for item in self.BLOCKED:

            if item in query:

                return FailResult(
                    error_message=f"Off-domain request: {item}"
                )

        return PassResult()