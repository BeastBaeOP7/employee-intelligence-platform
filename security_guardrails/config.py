"""
Central configuration for the Employee Intelligence Platform
Security Guardrails Engine.

This file should contain only configuration values.
No validation logic belongs here.
"""

from guardrails import OnFailAction

# ==========================================================
# General Settings
# ==========================================================

ENABLE_GUARDRAILS = True
ENABLE_AUDIT_LOGGING = True

# ==========================================================
# Guardrails AI Settings
# ==========================================================

DEFAULT_ON_FAIL = OnFailAction.EXCEPTION

TOXICITY_THRESHOLD = 0.80

# ==========================================================
# Enterprise Security Settings
# ==========================================================

BLOCK_PROMPT_INJECTION = True
BLOCK_SQL_INJECTION = True
BLOCK_ROLE_ESCALATION = True
BLOCK_OFF_DOMAIN = True
BLOCK_EXPORT_ESCALATION = True

# ==========================================================
# Output Protection
# ==========================================================

REDACT_EMAILS = True
REDACT_PASSWORDS = True
REDACT_SECRETS = True

# ==========================================================
# Allowed Export Roles
# ==========================================================

EXPORT_ALLOWED_ROLES = [
    "CEO",
    "HR_HEAD",
    "DEPT_DIRECTOR"
]

# ==========================================================
# Allowed Organization Roles
# ==========================================================

ORG_WIDE_ACCESS = [
    "CEO",
    "HR_HEAD"
]