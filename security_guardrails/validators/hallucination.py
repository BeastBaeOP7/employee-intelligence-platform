from guardrails_grhub_provenance_llm import ProvenanceLLM
from config.github_models_llm import get_llm


llm = get_llm()


def github_llm(prompt: str) -> str:
    """
    Uses the same GitHub Models LLM as the rest of the application.
    """
    return llm.invoke(prompt).content


class HallucinationValidator:

    def __init__(self):

        self.validator = ProvenanceLLM(
            validation_method="sentence",
            llm_callable=github_llm
        )

    def validate(self, response: str, context: str):

        metadata = {
            "sources": [context]
        }

        result = self.validator.validate(
            response,
            metadata
        )

        if result.outcome.name == "PASS":

            return {
                "allowed": True,
                "response": response
            }

        return {
            "allowed": False,
            "reason": result.error_message,
            "response": result.fix_value
        }