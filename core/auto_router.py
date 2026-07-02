"""
AUTO ROUTER v4 — with casual/small-talk tier
"""
from colorama import Fore, Style
from core.agent_dna import DNA

CASUAL_PATTERNS = [
    "hi", "hello", "hey", "yo", "sup", "good morning",
    "good evening", "good afternoon", "how are you",
    "thanks", "thank you", "ok", "okay", "cool", "nice",
    "bye", "goodbye", "see you", "good night", "yes",
    "no", "sure", "alright", "got it", "understood"
]

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
    "BE":    ["rest api", "backend", "api", "server", "database",
              "python script", "flask", "fastapi", "node",
              "endpoint", "crud", "sql", "postgresql", "django"],
    "FE":    ["website", "frontend", "html", "css", "react",
              "landing page", "webpage", "ui component",
              "nextjs", "tailwind"],
    "AIB":   ["ai agent", "chatbot", "llm", "build ai",
              "ai system", "prompt engineering", "automation",
              "rag", "vector"],
    "CR":    ["review code", "check code", "debug", "fix error",
              "code error", "bug fix", "why is this",
              "what is wrong"],
    "CONT":  ["blog", "article", "content", "write post",
              "social media post", "caption"],
    "LI":    ["linkedin", "b2b post", "professional post"],
    "IG":    ["instagram", "reel", "ig post", "hashtag"],
    "FB":    ["facebook", "fb post"],
    "EMAIL": ["email campaign", "cold email", "newsletter",
              "email sequence"],
    "SEO":   ["seo", "keyword", "search ranking", "google ranking"],
    "PROP":  ["proposal", "quote", "offer", "client brief",
              "write proposal"],
    "INV":   ["invoice", "bill", "payment", "charge client"],
    "BRAND": ["brand", "logo", "identity", "naming", "tagline"],
    "VID":   ["video", "script", "reel script", "youtube"],
    "DOC":   ["documentation", "readme", "docs", "manual"],
    "TEST":  ["test", "testing", "qa", "unit test", "test plan"],
    "MOB":   ["mobile app", "android", "ios", "flutter",
              "react native"],
    "SUP":   ["support", "complaint", "issue client", "help client"],
    "LEAD":  ["find leads", "leads", "prospects", "find clients"],
    "CRM":   ["follow up", "client relationship", "pipeline"],
    "SALES": ["sales script", "objection", "pitch", "close deal"],
    "FLUP":  ["follow up message", "re-engage", "ghosted"],
    "FAQ":   ["faq", "frequently asked"],
    "REV":   ["review", "testimonial", "collect feedback"],
    "CFA":   ["financial", "revenue", "profit", "cash flow", "budget"],
    "CLA":   ["legal", "contract", "compliance", "terms", "nda"],
    "CTO":   ["architecture", "tech stack", "infrastructure",
              "system architecture", "security audit"],
    "COA":   ["coordinate", "delegate", "organize", "operations"],
    "UI":    ["design system", "color palette", "typography",
              "wireframe", "mockup"],
    "UX":    ["user research", "user journey", "persona", "usability"],
    "GFX":   ["graphic", "banner", "poster", "design asset"],
    "ANA":   ["analyze data", "analytics", "kpi", "metrics",
              "data report"],
    "BOOK":  ["bookkeeping", "accounts", "financial records"],
    "EXP":   ["expense", "cut costs", "reduce spending"],
    "API":   ["integrate api", "api integration", "webhook"],
}

class AutoRouter:

    def __init__(self, brain):
        self.brain = brain

    def classify(self, prompt: str) -> dict:
        prompt_lower = prompt.strip().lower()
        word_count = len(prompt_lower.split())

        # 1. Casual/small-talk detection — highest priority
        # short message that IS or STARTS WITH a casual pattern
        if word_count <= 6:
            for pattern in CASUAL_PATTERNS:
                if prompt_lower == pattern or prompt_lower.startswith(pattern + " ") \
                   or prompt_lower.startswith(pattern + ","):
                    return {
                        "complexity": "CASUAL",
                        "agent": "COA",
                        "reason": "Greeting / small talk"
                    }

        # 2. Complex signals
        if any(sig in prompt_lower for sig in COMPLEX_SIGNALS):
            return {
                "complexity": "COMPLEX",
                "agent": "WORKFLOW",
                "reason": "Strategic decision — multi-department analysis needed"
            }

        # 3. Keyword match (longest match wins)
        best_match, best_len = None, 0
        for code, keywords in AGENT_KEYWORDS.items():
            for kw in keywords:
                if kw in prompt_lower and len(kw) > best_len:
                    best_match, best_len = code, len(kw)

        if best_match:
            return {
                "complexity": "SIMPLE",
                "agent": best_match,
                "reason": f"Keyword match → {DNA[best_match]['name']}"
            }

        # 4. Very short, non-matching input → treat as casual chat
        if word_count <= 4:
            return {
                "complexity": "CASUAL",
                "agent": "COA",
                "reason": "Short message, conversational"
            }

        # 5. LLM fallback for anything else
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
        complexity, agent, reason = "SIMPLE", "COA", "General request"
        for line in text.split("\n"):
            line = line.strip()
            upper = line.upper()
            if upper.startswith("COMPLEXITY:"):
                val = line.split(":",1)[1].strip().upper()
                complexity = "COMPLEX" if "COMPLEX" in val else "SIMPLE"
            elif upper.startswith("BEST_AGENT:"):
                val = (line.split(":",1)[1].strip().upper()
                       .replace("*","").replace("[","").replace("]","").strip())
                if val in DNA:
                    agent = val
                elif val == "WORKFLOW":
                    agent, complexity = "WORKFLOW", "COMPLEX"
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
