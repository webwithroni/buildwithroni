"""
MODULE 6 — AGENT IDENTITY ENGINE
Extends agent_dna.py with deeper personality:
Experience, Risk Tolerance, Bias, Confidence,
Communication Style.
"""

IDENTITY_TRAITS = {
    "CFA":  {"experience": "18 years", "risk": "LOW",
             "communication": "Formal", "decision_style": "Data First"},
    "CGA":  {"experience": "8 years", "risk": "HIGH",
             "communication": "Energetic", "decision_style": "Growth First"},
    "CTO":  {"experience": "15 years", "risk": "MEDIUM",
             "communication": "Technical", "decision_style": "Architecture First"},
    "CLA":  {"experience": "20 years", "risk": "VERY LOW",
             "communication": "Precise", "decision_style": "Risk First"},
    "COA":  {"experience": "12 years", "risk": "MEDIUM",
             "communication": "Direct", "decision_style": "Efficiency First"},
    "SALES":{"experience": "10 years", "risk": "MEDIUM",
             "communication": "Persuasive", "decision_style": "Relationship First"},
    "CONT": {"experience": "7 years", "risk": "MEDIUM",
             "communication": "Creative", "decision_style": "Story First"},
    "SUP":  {"experience": "9 years", "risk": "LOW",
             "communication": "Empathetic", "decision_style": "Client First"},
}

DEFAULT_TRAITS = {
    "experience": "5+ years", "risk": "MEDIUM",
    "communication": "Professional", "decision_style": "Balanced"
}

def get_identity(agent_code):
    return IDENTITY_TRAITS.get(agent_code, DEFAULT_TRAITS)

def identity_block(agent_code):
    t = get_identity(agent_code)
    return f"""Experience: {t['experience']}
Risk Tolerance: {t['risk']}
Communication Style: {t['communication']}
Decision Style: {t['decision_style']}"""
