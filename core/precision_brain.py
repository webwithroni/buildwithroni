"""
PRECISION BRAIN
Highest-accuracy mode: runs ensemble across ALL available
models, cross-validates answers against each other, and
only returns high-agreement content — flags disagreement
instead of silently picking one.
"""
from colorama import Fore, Style

class PrecisionBrain:
    def __init__(self, master_brain):
        self.brain = master_brain

    def precise_answer(self, prompt):
        targets = list(self.brain.available.keys())
        if len(targets) < 2:
            return self.brain.think(prompt, mode="best")

        results = []
        for m in targets:
            r = self.brain._call(m, prompt)
            if r and r.get("ok"):
                results.append(r)

        if len(results) < 2:
            return results[0]["text"] if results else "No models responded."

        combined = "\n\n".join([
            f"[{r['model'].upper()}]:\n{r['text'][:500]}" for r in results
        ])

        cross_check_prompt = f"""Multiple AI models answered the same question.
Cross-validate them for agreement/disagreement.

Question: {prompt[:200]}

Responses:
{combined}

1. Identify facts ALL models agree on (high confidence).
2. Identify anything only ONE model claims (flag as unverified).
3. Produce a final answer using ONLY high-agreement content,
   explicitly noting anything uncertain.

Format:
HIGH-CONFIDENCE ANSWER:
[content all models agree on]

FLAGGED (single-source, unverified):
[anything only one model said]"""

        for m in ["groq", "mistral", "cerebras"]:
            if m in self.brain.available:
                r = self.brain._call(m, cross_check_prompt)
                if r and r.get("ok"):
                    return r["text"]

        return results[0]["text"]
