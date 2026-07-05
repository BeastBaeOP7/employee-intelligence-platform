from guardrails.validator_base import (
    Validator,
    register_validator,
    PassResult,
    FailResult,
)


@register_validator(
    name="enterprise/export_policy",
    data_type="string",
)
class ExportPolicyValidator(Validator):

    def validate(self, value, metadata):

        role = metadata.get("role", "")

        query = value.lower()

        if "export" in query:

            if role not in [
                "CEO",
                "HR_HEAD",
                "DEPT_DIRECTOR",
            ]:

                return FailResult(
                    error_message="Export not permitted."
                )

        return PassResult()