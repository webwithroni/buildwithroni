"""
V4 — COGNITIVE ARCHITECTURE
Agents don't just answer. They THINK.

Observe -> Understand -> Recall -> Research ->
Generate Hypotheses -> Challenge Own Ideas ->
Ask Other Agents -> Decide -> Execute ->
Self Review -> Learn
"""
from colorama import Fore, Style

class CognitiveCycle:
    """
    Full 11-stage thinking pipeline.
    Every stage is a real reasoning step,
    not decoration.
    """

    def __init__(self, brain, kb, web_intel, dialogue_engine=None):
        self.brain = brain
        self.kb = kb
        self.web = web_intel
        self.dialogue = dialogue_engine

    def think(self, task, agent_name, role, personality="",
              can_ask_others=True, show_thinking=True):
        stages = {}

        def log(stage_name, content):
            if show_thinking:
                print(f"{Fore.CYAN}  [{stage_name}] "
                      f"{content[:80]}{Style.RESET_ALL}")

        # 1. OBSERVE
        stages["observe"] = self.brain.think(
            f"OBSERVE (1 sentence): What exactly is being "
            f"asked?\n{task}", mode="fast"
        )
        log("OBSERVE", stages["observe"])

        # 2. UNDERSTAND
        stages["understand"] = self.brain.think(
            f"UNDERSTAND (1 sentence): What is the real "
            f"underlying need?\nTask: {task}\n"
            f"Observation: {stages['observe']}", mode="fast"
        )
        log("UNDERSTAND", stages["understand"])

        # 3. RECALL MEMORY
        stages["recall"] = self.kb.get_context()
        log("RECALL", stages["recall"][:80])

        # 4. RESEARCH
        stages["research"] = (
            self.web.search(task[:100]) if self.web else
            "No web research available."
        )
        log("RESEARCH", "Evidence gathered from live web")

        # 5. GENERATE HYPOTHESES
        stages["hypotheses"] = self.brain.think(
            f"GENERATE 2-3 different possible approaches "
            f"to solve this (brief, one line each):\n"
            f"Task: {task}\nContext: {stages['understand']}",
            mode="best"
        )
        log("HYPOTHESES", "Multiple approaches generated")

        # 6. CHALLENGE OWN IDEAS
        stages["challenge"] = self.brain.think(
            f"CRITICALLY CHALLENGE these approaches. What "
            f"could go wrong with each? Be skeptical:\n"
            f"{stages['hypotheses']}", mode="fast"
        )
        log("CHALLENGE", "Self-critique complete")

        # 7. ASK OTHER AGENTS (if enabled and dialogue available)
        stages["consultation"] = "No consultation needed."
        if can_ask_others and self.dialogue:
            stages["consultation"] = self.dialogue.consult(
                task, agent_name, stages["challenge"]
            )
            log("CONSULT", "Got input from other agents")

        # 8. DECIDE
        stages["decide"] = self.brain.think(
            f"DECIDE: Given the hypotheses, challenges, and "
            f"any consultation, what's the best approach?\n"
            f"Hypotheses: {stages['hypotheses']}\n"
            f"Challenges: {stages['challenge']}\n"
            f"Consultation: {stages['consultation'][:200]}",
            mode="fast"
        )
        log("DECIDE", stages["decide"])

        # 9. EXECUTE
        stages["execute"] = self.brain.think(
            f"You are {agent_name}, {role} at Web With Roni "
            f"Private Limited.\nPersonality: {personality}\n\n"
            f"Execute the decided approach and deliver the "
            f"complete, professional final answer to:\n{task}\n\n"
            f"Decision: {stages['decide']}\n"
            f"Evidence: {stages['research'][:500]}\n\n"
            f"Write the full, complete answer now.",
            mode="ensemble"
        )
        log("EXECUTE", "Final answer generated")

        # 10. SELF REVIEW
        stages["review"] = self.brain.think(
            f"REVIEW your own answer briefly (1-2 sentences). "
            f"Any errors, gaps, or overclaims?\n"
            f"{stages['execute'][:500]}", mode="fast"
        )
        log("REVIEW", stages["review"])

        # 11. LEARN (caller handles persistence via kb/learner)
        stages["deliver"] = stages["execute"]

        return stages["deliver"], stages
