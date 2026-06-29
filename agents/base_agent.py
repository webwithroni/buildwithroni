from core.master_brain import MasterBrain
from core.knowledge_base import KnowledgeBase, COMPANY
from core.self_learner import SelfLearner
from core.agent_dna import DNA
from colorama import Fore, Style

_BRAIN = None
def get_brain():
    global _BRAIN
    if _BRAIN is None:
        _BRAIN = MasterBrain()
    return _BRAIN

class Agent:
    def __init__(self, key):
        self.key = key
        self.dna = DNA[key]
        self.brain = get_brain()
        self.kb = KnowledgeBase(key)
        self.learner = SelfLearner(key, self.brain)

    def think(self, task, context=""):
        print(f"\n{Fore.CYAN}🤖 {self.dna['name']} working...{Style.RESET_ALL}")

        skills = "\n".join([f"• {s}" for s in self.dna["skills"]])
        services = "\n".join([f"• {k}: {v}" for k,v in COMPANY["services"].items()])
        kb_ctx = self.kb.get_context()

        prompt = f"""You are {self.dna['name']} at Web With Roni Private Limited.
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

{f'Context: {context}' if context else ''}

TASK FROM RONI:
{task}

Deliver your absolute best work.
Be specific, professional, and actionable.
Format your response clearly."""

        mode = self.dna.get("style","best")
        response = self.brain.think(prompt, mode=mode)
        self._learn(task, response)
        return response

    def _learn(self, task, response):
        try:
            score = self.learner.score(
                task, response, self.dna["name"]
            )
            self.kb.add_task(task, response, score)

            if score >= 7.0:
                for p in self.learner.extract_patterns(task, response):
                    self.kb.add_pattern(p)

            if self.kb.count % 10 == 0 and self.kb.count > 0:
                note = self.learner.improve(
                    self.dna["name"], self.kb.data["tasks"]
                )
                if note:
                    self.kb.add_improvement(note)

            if self.kb.count % 25 == 0 and self.kb.count > 0:
                skill = self.learner.new_skill(
                    self.dna["name"], self.dna["skills"]
                )
                self.dna["skills"].append(skill)
                self.kb.add_skill(skill)
                print(f"{Fore.MAGENTA}⬆️  New skill unlocked: {skill}{Style.RESET_ALL}")

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
