import json
from guardrails.hub import GuardrailsPII
from validator import RestrictToTopic
from security_guardrails.validators.hallucination import HallucinationValidator
from security_guardrails.validators.sql_injection import SQLInjectionValidator
from security_guardrails.validators.prompt_injection import PromptInjectionValidator
from security_guardrails.validators.role_escalation import RoleEscalationValidator
#from security_guardrails.validators.off_domain import OffDomainValidator
from security_guardrails.validators.export_policy import ExportPolicyValidator
from config.github_models_llm import get_llm

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

        # Custom threshold function to prevent false positives for IPs, URLs, Driver Licenses
        def custom_threshold_fn(entity: str) -> float:
            if entity == "IP_ADDRESS":
                return 0.4
            elif entity == "US_DRIVER_LICENSE":
                return 0.4
            elif entity in ("URL", "DOMAIN_NAME"):
                return 0.4
            elif entity in ("LOCATION", "DATE_TIME", "PERSON", "PHONE_NUMBER"):
                return 0.75
            elif entity == "EMAIL_ADDRESS":
                return 0.8
            return 0.5

        # Normal PII (Masked but NOT blocked)
        self.pii_validator = GuardrailsPII(
            entities=[
                "EMAIL_ADDRESS", "PHONE_NUMBER", "PASSWORD", "USERNAME", 
                "API_KEY", "ACCESS_TOKEN", "SESSION_TOKEN", "SECRET"
            ],
            use_local=True,
            get_entity_threshold=custom_threshold_fn
        )

        # Sensitive Personal Info & Credentials (Masked and BLOCKED)
        self.spi_validator = GuardrailsPII(
            entities=[
                "CREDIT_CARD", "US_BANK_NUMBER", "IBAN_CODE", "US_SSN", 
                "US_PASSPORT", "US_DRIVER_LICENSE", "CVV", "SWIFT_CODE", 
                "AADHAAR_NUMBER", "PRIVATE_KEY", "JWT_TOKEN", "DB_CREDENTIAL",
                "CONNECTION_STRING", "ENCRYPTION_KEY", "OAUTH_TOKEN"
            ],
            use_local=True,
            get_entity_threshold=custom_threshold_fn
        )

        # Register custom Presidio recognizers to handle custom entities
        from presidio_analyzer import PatternRecognizer, Pattern
        
        custom_password_recognizer = PatternRecognizer(
            supported_entity="PASSWORD",
            patterns=[
                Pattern(name="db_passwords", regex=r"\b(ceo123|manager123|employee123)\b", score=1.0),
                Pattern(name="password_assignment", regex=r"(?i)password\s*[:=]\s*([a-zA-Z0-9_@#$!%-]{4,20})", score=0.8)
            ],
            context=["password", "pass", "pw"]
        )

        custom_username_recognizer = PatternRecognizer(
            supported_entity="USERNAME",
            patterns=[
                Pattern(name="username_assignment", regex=r"(?i)username\s*[:=]\s*([a-zA-Z0-9_-]{4,20})", score=0.8)
            ],
            context=["username", "user", "login"]
        )

        custom_apikey_recognizer = PatternRecognizer(
            supported_entity="API_KEY",
            patterns=[
                Pattern(name="api_key", regex=r"(?i)api[_-]key\s*[:=]\s*[a-zA-Z0-9_\-]{20,}", score=0.8)
            ],
            context=["api", "key"]
        )

        custom_accesstoken_recognizer = PatternRecognizer(
            supported_entity="ACCESS_TOKEN",
            patterns=[
                Pattern(name="access_token", regex=r"(?i)access[_-]token\s*[:=]\s*[a-zA-Z0-9_\-]{20,}", score=0.8)
            ],
            context=["access", "token"]
        )

        custom_sessiontoken_recognizer = PatternRecognizer(
            supported_entity="SESSION_TOKEN",
            patterns=[
                Pattern(name="session_token", regex=r"(?i)session[_-]token\s*[:=]\s*[a-zA-Z0-9_\-]{20,}", score=0.8)
            ],
            context=["session", "token"]
        )

        custom_secret_recognizer = PatternRecognizer(
            supported_entity="SECRET",
            patterns=[
                Pattern(name="env_secret", regex=r"(?i)(?:env|client)[_-]secret\s*[:=]\s*[a-zA-Z0-9_\-]{20,}", score=0.8)
            ],
            context=["secret", "env"]
        )

        custom_cvv_recognizer = PatternRecognizer(
            supported_entity="CVV",
            patterns=[
                Pattern(name="cvv_code", regex=r"\b\d{3,4}\b", score=0.4)
            ],
            context=["cvv", "cvc", "security code"]
        )

        custom_swift_recognizer = PatternRecognizer(
            supported_entity="SWIFT_CODE",
            patterns=[
                Pattern(name="swift_bank", regex=r"\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?\b", score=0.8)
            ],
            context=["swift", "bic", "swiftcode", "bankcode"]
        )

        custom_aadhaar_recognizer = PatternRecognizer(
            supported_entity="AADHAAR_NUMBER",
            patterns=[
                Pattern(name="aadhaar", regex=r"\b\d{4}\s\d{4}\s\d{4}\b", score=0.8),
                Pattern(name="aadhaar_flat", regex=r"\b\d{12}\b", score=0.7)
            ],
            context=["aadhaar", "aadhar", "uidai", "uid"]
        )

        custom_privatekey_recognizer = PatternRecognizer(
            supported_entity="PRIVATE_KEY",
            patterns=[
                Pattern(name="pem_private_key", regex=r"(?s)-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", score=1.0),
                Pattern(name="private_key_var", regex=r"(?i)private[_-]key\s*[:=]\s*\w{32,}", score=0.8)
            ],
            context=["privatekey", "key"]
        )

        custom_jwt_recognizer = PatternRecognizer(
            supported_entity="JWT_TOKEN",
            patterns=[
                Pattern(name="jwt", regex=r"\beyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_+/=]+\b", score=0.9)
            ],
            context=["jwt", "token"]
        )

        custom_dbcred_recognizer = PatternRecognizer(
            supported_entity="DB_CREDENTIAL",
            patterns=[
                Pattern(name="db_url", regex=r"\b(?:mongodb|postgresql|postgres|mysql|sqlite|oracle|sqlserver):\/\/[^\s]+", score=0.9)
            ],
            context=["db", "database", "connection", "conn", "credentials", "url"]
        )

        custom_oauth_recognizer = PatternRecognizer(
            supported_entity="OAUTH_TOKEN",
            patterns=[
                Pattern(name="oauth_tok", regex=r"(?i)oauth[_-]token\s*[:=]\s*[a-zA-Z0-9_\-\+/=]{20,}", score=0.8)
            ],
            context=["oauth", "token"]
        )

        custom_enc_recognizer = PatternRecognizer(
            supported_entity="ENCRYPTION_KEY",
            patterns=[
                Pattern(name="enc_key", regex=r"(?i)(?:encryption|secret)[_-]key\s*[:=]\s*[a-zA-Z0-9_\-\+/=]{20,}", score=0.8)
            ],
            context=["encryption", "key", "cipher"]
        )

        # Fallback card pattern (Luhn fails for seed mock data '1234567890123456')
        custom_cc_fallback_recognizer = PatternRecognizer(
            supported_entity="CREDIT_CARD",
            patterns=[
                Pattern(name="cc_weak", regex=r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b", score=0.8),
                Pattern(name="cc_weak_variable", regex=r"\b\d{13,19}\b", score=0.5)
            ],
            context=["credit card", "credit", "card", "debit card", "debit", "cc"]
        )

        for validator in [self.pii_validator, self.spi_validator]:
            registry = validator.pii_analyzer.registry
            registry.add_recognizer(custom_password_recognizer)
            registry.add_recognizer(custom_username_recognizer)
            registry.add_recognizer(custom_apikey_recognizer)
            registry.add_recognizer(custom_accesstoken_recognizer)
            registry.add_recognizer(custom_sessiontoken_recognizer)
            registry.add_recognizer(custom_secret_recognizer)
            registry.add_recognizer(custom_cvv_recognizer)
            registry.add_recognizer(custom_swift_recognizer)
            registry.add_recognizer(custom_aadhaar_recognizer)
            registry.add_recognizer(custom_privatekey_recognizer)
            registry.add_recognizer(custom_jwt_recognizer)
            registry.add_recognizer(custom_dbcred_recognizer)
            registry.add_recognizer(custom_oauth_recognizer)
            registry.add_recognizer(custom_enc_recognizer)
            registry.add_recognizer(custom_cc_fallback_recognizer)

        llm = get_llm()

        def github_topic_llm(text: str, topics: list[str]) -> str:
            topic_text = "\n".join(f"- {t}" for t in topics)
            prompt = f"""
You are a topic classification system.

Your job is to determine which of the candidate topics the user's query belongs to.

Rules:
- Return ONLY topics from the candidate list.
- If the query is unrelated to all topics, return an empty list.
- Do NOT invent new topics.
- Return ONLY valid JSON.

Examples:

User:
Tell me about Ryan Cooper

Output:
{{"topics_present":["Employee Profiles"]}}

User:
Who is the manager of the IT department?

Output:
{{"topics_present":["Department Analytics","Team Hierarchy"]}}

User:
Show promotion candidates

Output:
{{"topics_present":["Promotion Analysis"]}}

User:
Write a linked list in C++

Output:
{{"topics_present":[]}}

Candidate Topics:
{topic_text}

User Query:
{text}
"""
            print("\n===== PROMPT =====")
            print(prompt)
            print("==================")
            response = llm.invoke(prompt).content
            
            print("\n==== TOPIC VALIDATOR ====")
            print(response)
            response = response.replace("```json", "").replace("```", "").strip()

            data = json.loads(response)

            print("Parsed:", data)

            return data.get("topics_present", [])
            
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
            disable_classifier=True,
            disable_llm=False,
            llm_callable=github_topic_llm
        )

    def validate_input(self, query):
        for validator in self.input_validators:
            result = validator.validate(query, {})
            if result.outcome.name == "FAIL":
                return {
                    "allowed": False,
                    "reason": result.error_message
                }

        # Topic Restriction
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

    def validate_output(self, response, context, current_user=None):
        # Step 1: Mask normal PII
        text, pii_spans = self.pii_validator.anonymize(response, self.pii_validator.entities)

        # Step 2: Mask Sensitive PII on the text
        text, spi_spans = self.spi_validator.anonymize(text, self.spi_validator.entities)

        # If any Sensitive Personal Information or Credential is found, block and return sanitized response
        if len(spi_spans) > 0:
            return {
                "allowed": False,
                "reason": "Sensitive information detected",
                "response": text
            }

        # Step 3: Hallucination check on the sanitized text
        hallucination = self.hallucination_validator.validate(
            text,
            context
        )

        if not hallucination["allowed"]:
            return hallucination

        # Step 4: Export policy
        role = (current_user or {}).get("role", "")
        for validator in self.output_validators:
            result = validator.validate(response, {"role": role})
            if result.outcome.name == "FAIL":
                return {
                    "allowed": False,
                    "reason": result.error_message,
                    "response": text
                }

        return {
            "allowed": True,
            "response": text
        }


# Lazy singleton engine instance
_engine_instance: SecurityGuardrailsEngine = None

def get_engine() -> SecurityGuardrailsEngine:
    global _engine_instance
    if _engine_instance is None:
        print("[SecurityGuardrailsEngine] Initializing (one-time weight load)...")
        _engine_instance = SecurityGuardrailsEngine()
    return _engine_instance

# Module-level alias
engine = get_engine()