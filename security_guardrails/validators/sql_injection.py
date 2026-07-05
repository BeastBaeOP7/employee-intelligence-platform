from guardrails.validator_base import (
    Validator,
    register_validator,
    ValidationResult,
    PassResult,
    FailResult,
)


@register_validator(
    name="enterprise/sql_injection",
    data_type="string",
)
class SQLInjectionValidator(Validator):

    SQL_KEYWORDS = [
        "drop table",
        "delete from",
        "truncate table",
        "union select",
        "or 1=1",
        "insert into",
        "update set",
        "--",
        ";",
    ]

    def validate(self, value, metadata):

        query = value.lower()

        for keyword in self.SQL_KEYWORDS:

            if keyword in query:

                return FailResult(
                    error_message=f"SQL Injection detected: {keyword}"
                )

        return PassResult()