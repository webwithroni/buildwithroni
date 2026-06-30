"""
MODULE 1 (part 2) / MODULE 9 — CONFIDENCE ENGINE
Scores confidence based on evidence quality,
not just self-reported model certainty.
"""

class ConfidenceEngine:

    @staticmethod
    def calculate(has_web_evidence: bool,
                   model_self_score: float,
                   pattern_match: bool = False) -> dict:
        """
        Confidence is HIGHER when backed by real web data,
        LOWER when purely from model memory.
        """
        base = model_self_score * 10  # 0-100 scale

        if has_web_evidence:
            base = min(base + 20, 98)
            reason = "Backed by real-time web evidence"
        elif pattern_match:
            base = min(base + 5, 85)
            reason = "Matches previously learned patterns"
        else:
            base = max(base - 15, 10)
            reason = "Based on model training data only, no live verification"

        return {
            "score": round(base, 0),
            "reason": reason,
            "has_evidence": has_web_evidence
        }

    @staticmethod
    def format(confidence_dict):
        return (f"Confidence: {confidence_dict['score']}%\n"
                f"Reason: {confidence_dict['reason']}")
