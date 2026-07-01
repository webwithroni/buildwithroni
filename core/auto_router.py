"""
AUTO ROUTER v2 — Enterprise Grade
Reads any plain-language prompt and decides:
1. Which single expert agent handles it
2. Or whether full Project Titan workflow runs
"""
from colorama import Fore, Style
from core.agent_dna import DNA

COMPLEX_SIGNALS = [
    "should we", "should i", "strategy", "decide",
    "decision", "evaluate", "is it worth", "compare",
    "pros and cons", "full plan", "complete plan",
    "business case", "launch", "expand", "go to market",
    "risk analysis", "worth it", "recommend whether",
    "enterprise", "architecture", "system design",
    "full stack", "build company", "business plan",
    "phase", "roadmap", "invest"
]

AGENT_KEYWORDS = {
    "FE":    ["website", "frontend", "html", "css", "react",
              "ui", "landing page", "webpage"],
    "BE":    ["backend", "api", "server", "database", "python",
              "flask", "fastapi", "node", "endpoint"],
    "AIB":   ["ai agent", "chatbot", "llm", "build ai",
              "automation", "ai system", "prompt"],
    "CONT":  ["blog", "article", "content", "write", "post"],
    "LI":    ["linkedin", "b2b", "professional post"],
    "SEO":   ["seo", "keyword", "search ranking", "google"],
    "PROP":  ["proposal", "quote", "offer", "client brief"],
    "INV":   ["invoice", "bill", "payment", "charge"],
    "BRAND": ["brand", "logo", "identity", "naming"],
    "VID":   ["video", "script", "reel", "youtube"],
    "CR":    ["review code", "check code", "debug", "error"],
    "DOC":   ["documentation", "readme", "docs", "manual"],
    "SUP":   ["support", "complaint", "issue", "help client"],
    "LEAD":  ["leads", "prospects", "find clients", "outreach"],
    "EMAIL": ["email campaign", "cold email", "newsletter"],
    "CFA":   ["finance", "revenue", "profit", "cost analysis"],
    "CLA":   ["legal", "contract", "compliance", "terms"],
    "CTO":   ["architecture", "tech stack", "system design",
              "infrastructure", "security"],
    "COA":   ["plan", "coordinate", "organize", "delegate"],
    "TEST":  ["test", "testing", "qa", "bug", "quality"],
    "MOB":   ["mobile app", "android", "ios", "flutter",
              "react native"],
}

class AutoRouter:

    def __init__(self, brain):
        self.brain = brain

    def classify(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()

        # Fast heuristic — check complex signals first
        if any(sig in prompt_lower for sig in COMPLEX_SIGNALS):
            return {
                "complexity": "COMPLEX",
                "agent": "WORKFLOW",
                "reason": "Strategic/multi-department decision detected"
            }

        # Fast heuristic — direct keyword match
        for code, keywords in AGENT_KEYWORDS.items():
            if any(kw in prompt_lower for kw in keywords):
                return {
                    "complexity": "SIMPLE",
                    "agent": code,
                    "reason": f"Keyword match → {DNA[code]['name']}"
                }

        # LLM classification fallback (when heuristics don't match)
        agent_list = "\n".join([
            f"{code}: {DNA[code]['name']} — {DNA[code]['core']}"
            for code in DNA
        ])

        classify_prompt = f"""You are an expert router for an enterprise AI system.

Incoming request:
"{prompt}"

Available agents:
{agent_list}

Reply in EXACTLY this format:
COMPLEXITY: SIMPLE or COMPLEX
BEST_AGENT: ONE agent code (or WORKFLOW if complex)
REASON: one short sentence"""

        result = self.brain.think(classify_prompt, mode="fast")
        return self._parse(result)

    def _parse(self, text):
        complexity = "SIMPLE"
        agent = "COA"
        reason = "General request"

        for line in text.split("\n"):
            line = line.strip()
            upper = line.upper()

            if upper.startswith("COMPLEXITY:"):
                val = line.split(":", 1)[1].strip().upper()
                complexity = "COMPLEX" if "COMPLEX" in val else "SIMPLE"

            elif upper.startswith("BEST_AGENT:"):
                val = (line.split(":", 1)[1].strip()
                       .upper()
                       .replace("*","")
                       .replace("[","")
                       .replace("]","")
                       .strip())
                if val in DNA:
                    agent = val
                elif val == "WORKFLOW":
                    agent = "WORKFLOW"
                    complexity = "COMPLEX"
                else:
                    # fuzzy match
                    for code in DNA:
                        if code in val or val in code:
                            agent = code
                            break

            elif upper.startswith("REASON:"):
                reason = line.split(":", 1)[1].strip()

        if complexity == "COMPLEX":
            agent = "WORKFLOW"

        return {
            "complexity": complexity,
            "agent": agent,
            "reason": reason
        }
