"""
MODULE 2 — EXECUTIVE THINKING PIPELINE
Observe -> Understand -> Recall -> Research -> Plan ->
Brainstorm -> Critic -> Decide -> Execute -> Review -> Deliver
"""
from colorama import Fore, Style

class ThinkingPipeline:

    def __init__(self, agent_brain, kb, web_intel=None):
        self.brain = agent_brain
        self.kb = kb
        self.web = web_intel

    def run(self, task, agent_name, role):
        """Run the full 11-stage thinking pipeline"""
        print(f"{Fore.CYAN}🧠 {agent_name} entering deep thinking mode...{Style.RESET_ALL}")

        stages = {}

        stages["observe"]    = self.observe(task)
        stages["understand"] = self.understand(task, stages["observe"])
        stages["recall"]     = self.recall()
        stages["research"]   = self.research(task)
        stages["plan"]       = self.plan(task, stages)
        stages["brainstorm"] = self.brainstorm(task, stages)
        stages["critic"]     = self.critic(stages["brainstorm"])
        stages["decide"]     = self.decide(stages)
        stages["execute"]    = self.execute(task, stages, agent_name, role)
        stages["review"]     = self.review(stages["execute"])
        stages["deliver"]    = self.deliver(stages)

        print(f"{Fore.GREEN}✅ Deep thinking complete{Style.RESET_ALL}")
        return stages["deliver"], stages

    def observe(self, task):
        return self.brain.think(
            f"OBSERVE ONLY (1-2 sentences): What exactly is "
            f"being asked here?\n{task}", mode="fast"
        )

    def understand(self, task, observation):
        return self.brain.think(
            f"UNDERSTAND (1-2 sentences): What is the real "
            f"underlying need behind this?\nTask: {task}\n"
            f"Observation: {observation}", mode="fast"
        )

    def recall(self):
        return self.kb.get_context()

    def research(self, task):
        if self.web:
            return self.web.search(task[:100])
        return "No web research available for this task."

    def plan(self, task, stages):
        return self.brain.think(
            f"PLAN (brief): Given this task and context, "
            f"outline your approach in 3-4 bullet points.\n"
            f"Task: {task}\n"
            f"Understanding: {stages['understand']}", mode="fast"
        )

    def brainstorm(self, task, stages):
        return self.brain.think(
            f"BRAINSTORM: Generate 2-3 different approaches "
            f"to solve this task.\nTask: {task}\n"
            f"Plan: {stages['plan']}", mode="best"
        )

    def critic(self, brainstorm):
        return self.brain.think(
            f"CRITIC: Critically evaluate these approaches. "
            f"What are the weaknesses of each?\n{brainstorm}",
            mode="fast"
        )

    def decide(self, stages):
        return self.brain.think(
            f"DECIDE: Given the brainstormed options and "
            f"critique, which approach is best and why?\n"
            f"Options: {stages['brainstorm']}\n"
            f"Critique: {stages['critic']}", mode="fast"
        )

    def execute(self, task, stages, agent_name, role):
        return self.brain.think(
            f"You are {agent_name}, {role} at Web With Roni "
            f"Private Limited.\n\n"
            f"Now EXECUTE the chosen approach and deliver "
            f"the full, complete answer to:\n{task}\n\n"
            f"Decision made: {stages['decide']}\n"
            f"Research/Evidence: {stages['research'][:500]}\n\n"
            f"Write the complete, professional final answer now.",
            mode="ensemble"
        )

    def review(self, execution):
        return self.brain.think(
            f"REVIEW: Briefly check this answer for errors "
            f"or gaps (1-2 sentences):\n{execution[:500]}",
            mode="fast"
        )

    def deliver(self, stages):
        return stages["execute"]
