from guardrails.hub import GuardrailsPII
from validator import RestrictToTopic
from security_guardrails.validators.hallucination import HallucinationValidator
from security_guardrails.validators.sql_injection import SQLInjectionValidator
from security_guardrails.validators.prompt_injection import PromptInjectionValidator
from security_guardrails.validators.role_escalation import RoleEscalationValidator
from security_guardrails.validators.off_domain import OffDomainValidator
from security_guardrails.validators.export_policy import ExportPolicyValidator


class SecurityGuardrailsEngine:

    def __init__(self):

        self.input_validators = [
            SQLInjectionValidator(),
            PromptInjectionValidator(),
            RoleEscalationValidator(),
            # OffDomainValidator(),
        ]

        self.output_validators = [
            ExportPolicyValidator(),
        ]
        self.hallucination_validator = HallucinationValidator()

        self.pii_validator = GuardrailsPII(
            entities= "pii",
            use_local=True
        )
        self.spi_validator = GuardrailsPII(
            entities="spi",
            use_local=True
        )
        self.topic_validator = RestrictToTopic(
            valid_topics=[
                "Employee Profiles",
                "Salary Analytics",
                "Department Analytics",
                "Promotion Analysis",
                "Team Hierarchy",
                "Organization Reporting",
                "Employee Management",
                "Human Resources",
                "Organization Structure",
                "Excel Export Operations"
            ],
            disable_classifier=False,
            disable_llm=True
        )

    def validate_input(self, query):

        for validator in self.input_validators:

            result = validator.validate(query, {})

            if result.outcome.name == "FAIL":

                return {
                    "allowed": False,
                    "reason": result.error_message
                }

        # NEW: Restrict To Topic validator
        print("\n===== TOPIC VALIDATOR =====")
        print("Query:", query)

        result = self.topic_validator.validate(query, {})

        print("Outcome:", result.outcome)
        print("Message:", getattr(result, "error_message", None))
        print("===========================\n")
        
        if result.outcome.name == "FAIL":

            return {
                "allowed": False,
                "reason": result.error_message
            }

        return {
            "allowed": True
        }
    def validate_output(self, response, context):
        hallucination = self.hallucination_validator.validate(
            response,
            context
        )

        if not hallucination["allowed"]:
            return hallucination

        # Mask normal PII
        text, pii_spans = self.pii_validator.anonymize(
            response,
            self.pii_validator.entities
        )

        # Mask Sensitive PII
        text, spi_spans = self.spi_validator.anonymize(
            text,
            self.spi_validator.entities
        )

        all_spans = pii_spans + spi_spans

        if all_spans:
            return {
                "allowed": False,
                "reason": "Sensitive information detected",
                "response": text
            }

        for validator in self.output_validators:

            result = validator.validate(response, {})

            if result.outcome.name == "FAIL":

                return {
                    "allowed": False,
                    "reason": result.error_message
                }

        return {
            "allowed": True,
            "response": response
        }


engine = SecurityGuardrailsEngine()