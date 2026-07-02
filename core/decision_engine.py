"""
V8 — EXECUTIVE DECISION ENGINE
Every proposal gets scored across 8 dimensions.
CEO sees the ranked options with full transparency.

Dimensions: Revenue Impact, Risk, Cost, Time,
Confidence, Evidence, ROI, Difficulty
"""
from colorama import Fore, Style

DIMENSIONS = [
    "revenue_impact", "risk", "cost", "time",
    "confidence", "evidence", "roi", "difficulty"
]

WEIGHTS = {
    "revenue_impact": 0.20,
    "risk":           0.15,
    "cost":           0.10,
    "time":           0.10,
    "confidence":     0.15,
    "evidence":       0.15,
    "roi":            0.10,
    "difficulty":     0.05,
}

INVERTED = {"risk", "cost", "time", "difficulty"}


class DecisionEngine:

    def __init__(self, brain):
        self.brain = brain

    def score_proposal(self, proposal_name, proposal_text, context=""):
        prompt = f"""Score this business proposal across 8 dimensions.
Each score is 0-100.

Proposal: {proposal_name}
Details: {proposal_text[:600]}
Context: {context[:200]}

Score honestly:
REVENUE_IMPACT: [0-100, higher = more revenue potential]
RISK: [0-100, higher = MORE risky]
COST: [0-100, higher = MORE expensive]
TIME: [0-100, higher = takes LONGER]
CONFIDENCE: [0-100, higher = more certain this will work]
EVIDENCE: [0-100, higher = more evidence backing this]
ROI: [0-100, higher = better return on investment]
DIFFICULTY: [0-100, higher = MORE difficult to execute]

Reply with EXACTLY these 8 lines, numbers only after each colon."""

        result = self.brain.think(prompt, mode="fast")
        scores = self._parse_scores(result)
        final_score = self._calculate_final(scores)

        return {
            "name": proposal_name,
            "raw_scores": scores,
            "final_score": final_score
        }

    def _parse_scores(self, text):
        scores = {}
        for line in text.split("\n"):
            line = line.strip()
            if ":" not in line:
                continue
            key_raw, val_raw = line.split(":", 1)
            key = key_raw.strip().lower().replace(" ", "_")
            digits = ''.join(c for c in val_raw if c.isdigit())
            if key in DIMENSIONS and digits:
                scores[key] = min(max(int(digits), 0), 100)

        for dim in DIMENSIONS:
            scores.setdefault(dim, 50)

        return scores

    def _calculate_final(self, scores):
        total = 0
        for dim, weight in WEIGHTS.items():
            raw = scores.get(dim, 50)
            adjusted = (100 - raw) if dim in INVERTED else raw
            total += adjusted * weight
        return round(total, 1)

    def compare(self, proposals: dict, context=""):
        print(f"\n{Fore.MAGENTA}🎯 Executive Decision Engine — "
              f"scoring {len(proposals)} options...{Style.RESET_ALL}")

        results = []
        for name, text in proposals.items():
            print(f"{Fore.CYAN}  📊 Scoring: {name}...{Style.RESET_ALL}")
            scored = self.score_proposal(name, text, context)
            results.append(scored)

        ranked = sorted(results, key=lambda x: x["final_score"], reverse=True)

        print(f"\n{Fore.GREEN}{'─'*50}")
        print(f"  RANKED DECISION RESULTS")
        print(f"{'─'*50}{Style.RESET_ALL}")
        for i, r in enumerate(ranked, 1):
            marker = "👑" if i == 1 else f"{i}."
            print(f"  {marker} {r['name']} — "
                  f"Final Score: {r['final_score']}/100")

        return ranked

    def format_breakdown(self, scored_proposal):
        s = scored_proposal["raw_scores"]
        lines = [f"PROPOSAL: {scored_proposal['name']}",
                 f"FINAL SCORE: {scored_proposal['final_score']}/100",
                 ""]
        for dim in DIMENSIONS:
            label = dim.replace("_", " ").title()
            note = " (lower is better)" if dim in INVERTED else ""
            lines.append(f"  {label}{note}: {s.get(dim,50)}/100")
        return "\n".join(lines)
