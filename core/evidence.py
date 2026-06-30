"""
MODULE 1 (part 1) — EVIDENCE
Classifies and tracks evidence sources for claims.
"""

class Evidence:
    TYPES = ["FACT", "ASSUMPTION", "ESTIMATE",
             "UNKNOWN", "OPINION", "LIVE_DATA"]

    @staticmethod
    def from_web_search(has_web_data: bool) -> str:
        """Determine evidence type based on data source"""
        return "LIVE_DATA" if has_web_data else "ASSUMPTION"

    @staticmethod
    def format_claim(claim, evidence_type, source="", confidence=None):
        line = f"{evidence_type}: {claim}"
        if confidence is not None:
            line += f"\nConfidence: {confidence}%"
        if source:
            line += f"\nEvidence: {source}"
        return line
