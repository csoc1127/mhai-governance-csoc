"""
config.py
Central configuration for the MH-AI Dashboard
"""
import us
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR/ "data"

API_URL = "https://governing-ai-in-mental-health.digitalpsychpapers.org/api/bills?hide_excluded=true"
FALLBACK_CSV = DATA_DIR / "mh_ai_bills_raw.csv"

STATE_NAMES = {s.abbr: s.name for s in us.states.STATES}

#Ethics of care aligned tags - Tavory (2024) / Tronto's five elements

EOC_TAGS = [
    "vulnerable_populations",       # Fineman universal vulnerability — Tavory (2024)
    "safety_standards",             # Tronto attentiveness; duty of care
    "human_in_the_loop",            # Tavory: human connection option required
    "practitioner_responsibilities",# Tronto responsibility element; accountability
    "malpractice",                  # care-with; developers must bear consequences
    "event_reporting",              # Tronto responsiveness; monitoring how care lands
    "opt_out",                      # Tavory: non-negotiable right to human alternative
    "disclosure_consent",           # informed consent; NASW Code 1.03a
]


# Responsible AI aligned tags — standard regulatory framework
# Tavory (2024) argues these alone are insufficient — they protect autonomy and rights
# but ignore relational dependency, emotional vulnerability, and duty of care.
# Source definitions: Shumate et al. (2025) Table 2
RESPONSIBLE_AI_TAGS = [
    "civil_penalties",             # Noncriminal penalties — system suspension, fines, private
                                   # right of action, profit disgorgement
    "consumer_protection",         # Fraudulent/manipulative/deceptive use of MH-AI including
                                   # in advertising
    "criminal_penalties",          # Criminal fines, incarceration, misdemeanor/felony
    "data_protection",             # Privacy, security, retention/deletion — encryption,
                                   # secure storage, data purging
    "discrimination_bias",         # Requirements re: discrimination, bias, or fairness
    "licensing_board_oversight",   # State professional licensing board oversight of MH-AI
    "meta_biometric_data",         # Biometric, behavioral, or metadata regulation
    "monitoring",                  # Audits, documentation, reports, postmarket surveillance
    "payments_insurance",          # Insurance coverage, reimbursement, payment models
    "pilot_sandbox",               # Regulatory pilot programs / sandbox testing pre-market
    "post_market_review",          # Scheduled review after AI product marketed/implemented
    "pre_market_review",           # Regulatory review before AI product offered
    "prescribing",                 # Requirements/waivers re: prescriptions
    "research",                    # Data collection, consent, ethical guidelines for research
    "risk_classification",         # High-risk AI system frameworks, consequential decisions
    "special_purpose_entities",    # Committees, task forces, subcommittees re: MH-AI
    "transparency",                # Public/patient rights to access AI system data,
                                   # public inventories, publication requirements
]

