"""
EVOLUTION ENGINE
Runs after every task: awards experience, checks if a
new skill was earned, logs episodic memory, and reports
what changed — the visible "self-improvement" loop.
"""
from colorama import Fore, Style
from core.experience import Experience
from core.skill_factory import SkillFactory
from core.memory_advanced import AdvancedMemory

class EvolutionEngine:
    def __init__(self, brain):
        self.brain = brain
        self.skill_factory = SkillFactory(brain)

    def process(self, agent_code, agent_name, task, response,
                score, current_skills):
        exp = Experience(agent_code)
        mem = AdvancedMemory(agent_code)

        gained, leveled_up, level = exp.award(score, task_type="task")
        mem.remember_short(f"Handled: {task[:80]}")
        mem.log_episode(task[:100], outcome=f"score {score}/10")

        new_skill = self.skill_factory.generate_if_earned(
            agent_code, agent_name, current_skills, task
        )

        report = {
            "xp_gained": gained,
            "leveled_up": leveled_up,
            "new_level": level,
            "new_skill": new_skill
        }

        if leveled_up:
            print(f"{Fore.MAGENTA}🎖️  {agent_name} leveled up → "
                  f"{level}!{Style.RESET_ALL}")
        if new_skill:
            print(f"{Fore.GREEN}⬆️  {agent_name} earned skill: "
                  f"{new_skill}{Style.RESET_ALL}")

        return report
