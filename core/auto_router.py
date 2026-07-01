"""
AUTO ROUTER v3 — Fixed keyword mapping
"""
from colorama import Fore, Style
from core.agent_dna import DNA

COMPLEX_SIGNALS = [
    "should we", "should i", "strategy", "decide",
    "decision", "evaluate", "is it worth", "compare",
    "pros and cons", "full plan", "complete plan",
    "business case", "launch", "expand", "go to market",
    "risk analysis", "worth it", "recommend whether",
    "enterprise", "system design", "business plan",
    "phase", "roadmap", "invest", "pricing strategy",
    "market entry", "hire", "partnership"
]

AGENT_KEYWORDS = {
    "BE":    ["rest api", "backend", "api", "server",
              "database", "python script", "flask",
              "fastapi", "node", "endpoint", "crud",
              "sql", "postgresql", "django"],
    "FE":    ["website", "frontend", "html", "css",
              "react", "landing page", "webpage",
              "ui component", "nextjs", "tailwind"],
    "AIB":   ["ai agent", "chatbot", "llm", "build ai",
              "ai system", "prompt engineering",
              "automation", "rag", "vector"],
    "CR":    ["review code", "check code", "debug",
              "fix error", "code error", "bug fix",
              "why is this", "what is wrong"],
    "CONT":  ["blog", "article", "content", "write post",
              "social media post", "caption"],
    "LI":    ["linkedin", "b2b post", "professional post",
              "linkedin post"],
    "IG":    ["instagram", "reel", "ig post", "hashtag"],
    "FB":    ["facebook", "fb post", "facebook post"],
    "EMAIL": ["email campaign", "cold email", "newsletter",
              "email sequence"],
    "SEO":   ["seo", "keyword", "search ranking",
              "google ranking", "organic traffic"],
    "PROP":  ["proposal", "quote", "offer", "client brief",
              "write proposal"],
    "INV":   ["invoice", "bill", "payment", "charge client"],
    "BRAND": ["brand", "logo", "identity", "naming",
              "tagline", "brand identity", "brand colors"],
    "VID":   ["video", "script", "reel script", "youtube",
              "video script"],
    "DOC":   ["documentation", "readme", "docs", "manual",
              "write docs"],
    "TEST":  ["test", "testing", "qa", "unit test",
              "write tests", "test plan"],
    "MOB":   ["mobile app", "android", "ios", "flutter",
              "react native", "app"],
    "SUP":   ["support", "complaint", "issue client",
              "help client", "client problem"],
    "LEAD":  ["find leads", "leads", "prospects",
              "find clients", "outreach list"],
    "CRM":   ["follow up", "client relationship",
              "pipeline", "crm"],
    "SALES": ["sales script", "objection", "pitch",
              "discovery call", "close deal"],
    "FLUP":  ["follow up message", "re-engage",
              "ghosted", "no response"],
    "FAQ":   ["faq", "frequently asked", "common questions"],
    "REV":   ["review", "testimonial", "collect feedback",
              "review request"],
    "CFA":   ["financial", "revenue", "profit", "cash flow",
              "cost analysis", "budget"],
    "CLA":   ["legal", "contract", "compliance", "terms",
              "agreement", "nda"],
    "CTO":   ["architecture", "tech stack", "infrastructure",
              "system architecture", "security audit"],
    "COA":   ["plan", "coordinate", "delegate", "organize",
              "operations"],
    "UI":    ["design system", "color palette", "typography",
              "figma", "wireframe", "mockup"],
    "UX":    ["user research", "user journey", "persona",
              "usability", "ux"],
    "GFX":   ["graphic", "banner", "poster", "social graphic",
              "design asset"],
    "ANA":   ["analyze data", "analytics", "kpi", "metrics",
              "data report", "performance report"],
    "BOOK":  ["bookkeeping", "accounts", "expenses",
              "financial records"],
    "EXP":   ["expense", "cut costs", "reduce spending",
              "budget optimization"],
    "API":   ["integrate api", "api integration", "webhook",
              "third party api", "connect api"],
}

class AutoRouter:

    def __init__(self, brain):
        self.brain = brain

    def classify(self, prompt: str) -> dict:
        prompt_lower = prompt.lower()

        # 1. Complex signals check first
        if any(sig in prompt_lower for sig in COMPLEX_SIGNALS):
            return {
                "complexity": "COMPLEX",
                "agent": "WORKFLOW",
                "reason": "Strategic decision — multi-department analysis needed"
            }

        # 2. Keyword match (longest match wins)
        best_match = None
        best_len = 0
        for code, keywords in AGENT_KEYWORDS.items():
            for kw in keywords:
                if kw in prompt_lower and len(kw) > best_len:
                    best_match = code
                    best_len = len(kw)

        if best_match:
            return {
                "complexity": "SIMPLE",
                "agent": best_match,
                "reason": f"Keyword match → {DNA[best_match]['name']}"
            }

        # 3. LLM fallback
        agent_list = "\n".join([
            f"{code}: {DNA[code]['name']} — {DNA[code]['core']}"
            for code in DNA
        ])
        classify_prompt = f"""Route this request to the best specialist:
"{prompt}"

Agents:
{agent_list}

Reply EXACTLY:
COMPLEXITY: SIMPLE or COMPLEX
BEST_AGENT: code or WORKFLOW
REASON: one sentence"""

        result = self.brain.think(classify_prompt, mode="fast")
        return self._parse(result)

    def _parse(self, text):
        complexity = "SIMPLE"
        agent = "COA"
        reason = "General request"

        for line in text.split("\n"):
            line  = line.strip()
            upper = line.upper()
            if upper.startswith("COMPLEXITY:"):
                val = line.split(":",1)[1].strip().upper()
                complexity = "COMPLEX" if "COMPLEX" in val else "SIMPLE"
            elif upper.startswith("BEST_AGENT:"):
                val = (line.split(":",1)[1].strip()
                       .upper()
                       .replace("*","").replace("[","").replace("]","")
                       .strip())
                if val in DNA:
                    agent = val
                elif val == "WORKFLOW":
                    agent = "WORKFLOW"
                    complexity = "COMPLEX"
                else:
                    for code in DNA:
                        if code in val or val in code:
                            agent = code
                            break
            elif upper.startswith("REASON:"):
                reason = line.split(":",1)[1].strip()

        if complexity == "COMPLEX":
            agent = "WORKFLOW"
        return {"complexity": complexity, "agent": agent, "reason": reason}
