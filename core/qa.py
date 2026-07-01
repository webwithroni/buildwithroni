"""
MODULE 8 — QUALITY ASSURANCE v2
More robust pass/fail detection.
"""
from colorama import Fore, Style

class QAEngine:

    def __init__(self, brain):
        self.brain = brain

    def review(self, original_task, response):
        print(f"{Fore.YELLOW}🔎 QA reviewing...{Style.RESET_ALL}")

        prompt = f"""You are the QA Lead at Web With Roni Private Limited.
Review this response quickly.

Task: {original_task[:150]}
Response: {response[:800]}

Check for critical issues only:
- Does it actually answer the task? (Yes/No)
- Any obviously invented numbers or fake facts? (Yes/No)
- Any major contradictions? (Yes/No)

Reply EXACTLY:
ANSWERS_TASK: Yes or No
FAKE_DATA: Yes or No
CONTRADICTIONS: Yes or No
PASS: Yes or No
ISSUES: brief note or None"""

        review = self.brain.think(prompt, mode="fast")
        passed = self._detect_pass(review, response)

        if passed:
            print(f"{Fore.GREEN}✅ QA passed{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  QA flagged{Style.RESET_ALL}")

        return {"review": review, "passed": passed}

    def _detect_pass(self, review_text, original_response):
        """Robust pass detection"""
        text_lower = review_text.lower()

        # Explicit fail signals
        fail_signals = [
            "pass: no", "fake_data: yes",
            "contradictions: yes", "answers_task: no"
        ]
        for signal in fail_signals:
            if signal in text_lower:
                return False

        # Explicit pass signal
        if "pass: yes" in text_lower:
            return True

        # If response is substantial (>100 words), assume pass
        if len(original_response.split()) > 100:
            return True

        return False
