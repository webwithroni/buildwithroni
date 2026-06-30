"""
MODULE 1 — TRUTH GUARD ENGINE
Agent -> Fact Checker -> Evidence Validator ->
Confidence Score -> Final Report

Prevents agents from inventing fake facts/numbers.
"""
from core.evidence import Evidence
from core.confidence import ConfidenceEngine
from colorama import Fore, Style

class TruthGuard:
    """
    Validates agent output, classifies every claim,
    and attaches confidence scores before delivery.
    """

    def __init__(self, brain):
        self.brain = brain

    def validate(self, response, has_web_evidence,
                 model_self_score=7.0):
        """
        Run the response through truth classification.
        Returns enriched response + confidence metadata.
        """
        print(f"{Fore.YELLOW}🔍 Truth Guard checking response...{Style.RESET_ALL}")

        confidence = ConfidenceEngine.calculate(
            has_web_evidence, model_self_score
        )

        # Ask the model to self-classify its key claims
        check_prompt = f"""You wrote this response:
{response[:1000]}

Classify the TOP 3 most important factual claims
in your response. For each, label as one of:
FACT, ASSUMPTION, ESTIMATE, UNKNOWN, OPINION, LIVE_DATA

Format EXACTLY like this for each:
CLAIM: [the claim]
TYPE: [classification]
REASON: [why this classification]

If you have no real evidence for a number/fact,
you MUST mark it ASSUMPTION or ESTIMATE — never FACT."""

        classification = self.brain.think(check_prompt, mode="fast")

        result = f"""{response}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ TRUTH GUARD VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{classification}

{ConfidenceEngine.format(confidence)}
Evidence Source: {"Real-time web search" if has_web_evidence else "Model knowledge (unverified)"}
"""
        print(f"{Fore.GREEN}✅ Truth Guard complete — "
              f"{confidence['score']}% confidence{Style.RESET_ALL}")

        return result, confidence
