"""
EXPERIENCE SYSTEM
Agents accumulate experience points and level up
seniority based on QUALITY of work, not just task count.
"""
import json, os
from datetime import datetime

EXP_DIR = "knowledge/experience"
os.makedirs(EXP_DIR, exist_ok=True)

LEVELS = [
    (0,    "Junior"),
    (100,  "Associate"),
    (300,  "Mid-Level"),
    (700,  "Senior"),
    (1500, "Principal"),
    (3000, "Distinguished"),
]

class Experience:
    def __init__(self, agent_code):
        self.code = agent_code
        self.path = f"{EXP_DIR}/{agent_code}.json"
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {"xp": 0, "level": "Junior", "history": []}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def award(self, score: float, task_type="general"):
        """
        score is the QA/truth-guard confidence-adjusted
        quality score (0-10). XP scales with quality,
        not just completion.
        """
        gained = round(score * 3)  # up to 30 xp per high-quality task
        self.data["xp"] += gained
        self.data["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "gained": gained, "score": score, "type": task_type
        })
        self.data["history"] = self.data["history"][-200:]

        new_level = "Junior"
        for threshold, name in LEVELS:
            if self.data["xp"] >= threshold:
                new_level = name
        leveled_up = new_level != self.data["level"]
        self.data["level"] = new_level
        self.save()
        return gained, leveled_up, new_level

    def status(self):
        return {"xp": self.data["xp"], "level": self.data["level"]}
