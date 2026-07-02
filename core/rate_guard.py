import time
from colorama import Fore, Style

class RateGuard:
    """Wraps brain.think with retry+backoff, tracks call count."""
    def __init__(self, brain, budget_per_session=150):
        self.brain = brain
        self.calls = 0
        self.budget = budget_per_session

    def think(self, prompt, mode="best", retries=3):
        if self.calls >= self.budget:
            return "⚠️ Session call budget reached. Try again shortly."
        for attempt in range(retries):
            self.calls += 1
            result = self.brain.think(prompt, mode=mode)
            if result and "All models failed" not in result:
                return result
            wait = (attempt + 1) * 3
            print(f"{Fore.YELLOW}Rate guard retry in {wait}s{Style.RESET_ALL}")
            time.sleep(wait)
        return "⚠️ All models temporarily unavailable. Try again in a minute."

    def status(self):
        return {"calls_used": self.calls, "budget": self.budget}
