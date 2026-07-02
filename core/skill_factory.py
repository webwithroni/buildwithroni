"""
SKILL FACTORY
Generates NEW skills for agents based on ACTUAL task
patterns encountered — not an arbitrary fixed count.

Realistic budget: each agent can gain up to 3 new
skills per day, triggered only when the agent has
handled enough real tasks to justify it. This respects
free-tier API limits (38 agents x 3 = max 114 skill-gen
calls/day, not 38,000).
"""
import json, os
from datetime import datetime

SKILL_LOG = "knowledge/skill_factory_log.json"
DAILY_CAP_PER_AGENT = 3

class SkillFactory:
    def __init__(self, brain):
        self.brain = brain
        self.log = self._load()

    def _load(self):
        if os.path.exists(SKILL_LOG):
            with open(SKILL_LOG) as f:
                return json.load(f)
        return {}

    def _save(self):
        with open(SKILL_LOG, "w") as f:
            json.dump(self.log, f, indent=2)

    def _today_count(self, agent_code):
        today = datetime.now().strftime("%Y-%m-%d")
        return len([
            e for e in self.log.get(agent_code, [])
            if e["date"] == today
        ])

    def generate_if_earned(self, agent_code, agent_name,
                            current_skills, recent_task_summary):
        """
        Only generates a skill if:
        - daily cap not reached
        - recent tasks suggest a genuine gap
        """
        if self._today_count(agent_code) >= DAILY_CAP_PER_AGENT:
            return None

        prompt = f"""You are {agent_name}. Current skills:
{', '.join(current_skills[:8])}

Recent work pattern: {recent_task_summary[:300]}

Based on ACTUAL recent work (not hypothetically), is there
ONE new specific skill worth adding? Only answer if there's
a genuine, evidenced gap — otherwise say NONE.

Format: SKILL: [specific skill name] or NONE"""

        result = self.brain.think(prompt, mode="fast")
        if "NONE" in result.upper() and "SKILL:" not in result.upper():
            return None

        skill_name = None
        for line in result.split("\n"):
            if "SKILL:" in line.upper():
                skill_name = line.split(":", 1)[1].strip()
                break

        if not skill_name or skill_name in current_skills:
            return None

        self.log.setdefault(agent_code, []).append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "skill": skill_name
        })
        self._save()
        return skill_name
