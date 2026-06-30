"""
MODULE 3 — DEBATE ENGINE
Business -> Marketing -> Finance -> Engineering ->
Legal -> Support -> Conflict -> Resolution -> Decision
"""
from colorama import Fore, Style
from agents.base_agent import Agent

class DebateEngine:

    DEBATERS = {
        "Business":    "SALES",
        "Marketing":   "CGA",
        "Finance":     "CFA",
        "Engineering": "CTO",
        "Legal":       "CLA",
        "Support":     "SUP",
    }

    def __init__(self, brain):
        self.brain = brain

    def debate(self, topic: str) -> dict:
        """
        Each department gives its opinion on a topic.
        Conflicts identified. Executive decides.
        """
        print(f"{Fore.MAGENTA}🗣️  Debate starting on: {topic[:50]}...{Style.RESET_ALL}")

        opinions = {}
        for dept, agent_code in self.DEBATERS.items():
            print(f"{Fore.CYAN}  → {dept} forming opinion...{Style.RESET_ALL}")
            agent = Agent(agent_code)
            opinion = agent.think(
                f"From your {dept} perspective, give your honest "
                f"professional opinion on this decision:\n{topic}\n"
                f"State your position clearly, your top concern, "
                f"and what you'd prioritize. Be direct, 3-4 sentences."
            )
            opinions[dept] = opinion

        conflict_matrix = self._find_conflicts(topic, opinions)
        decision = self._executive_decision(topic, opinions, conflict_matrix)

        return {
            "topic": topic,
            "opinions": opinions,
            "conflicts": conflict_matrix,
            "decision": decision
        }

    def _find_conflicts(self, topic, opinions):
        combined = "\n\n".join([
            f"[{dept}]: {op[:300]}" for dept, op in opinions.items()
        ])

        prompt = f"""Topic: {topic}

Department opinions:
{combined}

Identify any CONFLICTS or tensions between departments.
Format as:
CONFLICT: [dept A] vs [dept B]
ISSUE: [what they disagree on]

If departments are aligned, say "NO MAJOR CONFLICTS — departments aligned"."""

        print(f"{Fore.YELLOW}⚖️  Analyzing conflicts...{Style.RESET_ALL}")
        return self.brain.think(prompt, mode="fast")

    def _executive_decision(self, topic, opinions, conflicts):
        combined = "\n\n".join([
            f"[{dept}]: {op[:300]}" for dept, op in opinions.items()
        ])

        prompt = f"""You are the Chief Operating Agent making the
final executive decision at Web With Roni Private Limited.

Topic: {topic}

Department opinions:
{combined}

Identified conflicts:
{conflicts}

Make the FINAL EXECUTIVE DECISION. Weigh all department
input, resolve conflicts, and give Roni one clear
recommendation with reasoning."""

        print(f"{Fore.MAGENTA}👑 Executive deciding...{Style.RESET_ALL}")
        return self.brain.think(prompt, mode="ensemble")
