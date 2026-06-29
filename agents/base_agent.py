"""
BASE AGENT — WITH REAL-TIME WEB INTELLIGENCE
Every agent now has live internet access.
Searches web automatically when needed.
"""
from core.master_brain import MasterBrain
from core.knowledge_base import KnowledgeBase, COMPANY
from core.self_learner import SelfLearner
from core.agent_dna import DNA
from core.web_intel import WebIntel
from colorama import Fore, Style

_BRAIN = None
_WEB = None

def get_brain():
    global _BRAIN
    if _BRAIN is None:
        _BRAIN = MasterBrain()
    return _BRAIN

def get_web():
    global _WEB
    if _WEB is None:
        _WEB = WebIntel()
    return _WEB

# Tasks that need web search
WEB_TRIGGERS = [
    "latest", "current", "today", "news", "2026",
    "price", "cost", "trend", "competitor", "market",
    "research", "find", "search", "what is", "how much",
    "best", "top", "compare", "review", "recent",
    "leads", "prospect", "client", "industry"
]

class Agent:
    def __init__(self, key):
        self.key     = key
        self.dna     = DNA[key]
        self.brain   = get_brain()
        self.kb      = KnowledgeBase(key)
        self.learner = SelfLearner(key, self.brain)
        self.web     = get_web()

    def think(self, task, context="", use_web=None):
        """
        Core thinking with optional web search.
        Auto-detects if web search is needed.
        """
        print(f"\n{Fore.CYAN}🤖 {self.dna['name']} working...{Style.RESET_ALL}")

        # Auto-detect if web search needed
        needs_web = use_web
        if needs_web is None:
            task_lower = task.lower()
            needs_web = any(t in task_lower for t in WEB_TRIGGERS)

        # Get web context if needed
        web_context = ""
        if needs_web:
            web_context = self.web.search(task[:100])
            print(f"{Fore.GREEN}🌐 Web data acquired{Style.RESET_ALL}")

        # Build full prompt
        prompt = self._build_prompt(task, context, web_context)

        # Think with master brain
        mode = self.dna.get("style", "best")
        response = self.brain.think(prompt, mode=mode)

        # Learn from task
        self._learn(task, response)

        return response

    def think_with_web(self, task, context=""):
        """Force web search for this task"""
        return self.think(task, context, use_web=True)

    def think_fast(self, task):
        """Quick answer, no web search"""
        return self.think(task, use_web=False)

    def _build_prompt(self, task, context, web_context):
        skills = "\n".join([f"• {s}" for s in self.dna["skills"]])
        services = "\n".join([
            f"• {k}: {v}" for k,v in COMPANY["services"].items()
        ])
        kb_ctx = self.kb.get_context()

        web_section = ""
        if web_context:
            web_section = f"""
REAL-TIME WEB DATA (use this for current information):
{web_context}
"""

        return f"""You are {self.dna['name']} at Web With Roni Private Limited.
Department: {self.dna['dept']}
Personality: {self.dna['personality']}
Core Mission: {self.dna['core']}

Your Expertise:
{skills}

Company: Web With Roni Private Limited
Founder: Roni (the only human — your boss)
Services:
{services}

Your Learning History:
{kb_ctx}
{web_section}
{f'Additional Context: {context}' if context else ''}

TASK FROM RONI:
{task}

Deliver your absolute best work.
Use real-time web data above if provided.
Be specific, professional, and actionable.
Cite current information where relevant."""

    def _learn(self, task, response):
        try:
            score = self.learner.score(
                task, response, self.dna["name"]
            )
            self.kb.add_task(task, response, score)

            if score >= 7.0:
                for p in self.learner.extract_patterns(
                    task, response
                ):
                    self.kb.add_pattern(p)

            if self.kb.count % 10 == 0 and self.kb.count > 0:
                note = self.learner.improve(
                    self.dna["name"],
                    self.kb.data["tasks"]
                )
                if note:
                    self.kb.add_improvement(note)

            if self.kb.count % 25 == 0 and self.kb.count > 0:
                skill = self.learner.new_skill(
                    self.dna["name"],
                    self.dna["skills"]
                )
                self.dna["skills"].append(skill)
                self.kb.add_skill(skill)
                print(f"{Fore.MAGENTA}⬆️ New skill: "
                      f"{skill}{Style.RESET_ALL}")

            print(f"{Fore.GREEN}📚 Score: {score:.1f}/10 | "
                  f"Tasks: {self.kb.count} | "
                  f"v{self.kb.version}{Style.RESET_ALL}")
        except:
            pass

    def status(self):
        return {
            "name":    self.dna["name"],
            "key":     self.key,
            "dept":    self.dna["dept"],
            "tasks":   self.kb.count,
            "version": self.kb.version,
            "skills":  len(self.dna["skills"]),
        }
