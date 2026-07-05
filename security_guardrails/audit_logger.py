import json
from datetime import datetime


LOG_FILE = "logs/guardrail_audit.log"


def log_guardrail_event(
    user: str,
    role: str,
    query: str,
    decision: str,
    reason: str
):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "user": user,
        "role": role,
        "query": query,
        "decision": decision,
        "reason": reason
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")