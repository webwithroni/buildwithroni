"""
MODULE 8 — QUALITY ASSURANCE
Agent -> QA Agent -> Truth Guard -> Executive
"""
from colorama import Fore, Style

class QAEngine:

    def __init__(self, brain):
        self.brain = brain

    def review(self, original_task, response):
        """
        QA pass checking for issues before delivery.
        """
        print(f"{Fore.YELLOW}🔎 QA reviewing response...{Style.RESET_ALL}")

        prompt = f"""You are the QA Lead at Web With Roni Private Limited.
Review this response for quality issues.

Original task: {original_task[:200]}

Response to review:
{response[:1500]}

Check for:
- Missing data (did it skip parts of the task?)
- Fake/invented data (unverified numbers stated as fact)
- Contradictions (does it contradict itself?)
- Grammar/clarity issues
- Logic errors
- Missing evidence for claims
- Formatting problems

Format your review as:
ISSUES FOUND: [list any issues, or "None"]
SEVERITY: [Low/Medium/High]
PASS: [Yes/No]
RECOMMENDATION: [what to fix, if anything]"""

        review = self.brain.think(prompt, mode="fast")

        passed = "PASS: Yes" in review or "pass: yes" in review.lower()

        if passed:
            print(f"{Fore.GREEN}✅ QA passed{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}⚠️  QA flagged issues{Style.RESET_ALL}")

        return {
            "review": review,
            "passed": passed
        }
