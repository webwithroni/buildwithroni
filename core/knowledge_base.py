import json, os
from datetime import datetime

KB_DIR = "knowledge/agents"
os.makedirs(KB_DIR, exist_ok=True)

COMPANY = {
    "name":    "Web With Roni Private Limited",
    "short":   "Web With Roni",
    "founder": "Roni",
    "email":   "webwithroni@gmail.com",
    "website": "webwithroni.vercel.app",
    "mission": "Enterprise-grade AI delivery",
    "services": {
        "3-page website":   "$500 / 7 days",
        "5-page website":   "$1,000 / 10 days",
        "ecommerce store":  "$2,500 / 14 days",
        "web application":  "$5,000+ / 30 days",
        "ai integration":   "$3,000 / 10 days",
        "monthly retainer": "$500/month"
    }
}

class KnowledgeBase:
    def __init__(self, code):
        self.code = code
        self.path = f"{KB_DIR}/{code}.json"
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {
            "code": self.code,
            "created": datetime.now().isoformat(),
            "version": 1,
            "tasks": [],
            "patterns": [],
            "skills": [],
            "improvements": [],
            "scores": []
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_task(self, task, response, score=None):
        self.data["tasks"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "task": task[:200],
            "preview": response[:300],
            "score": score
        })
        if len(self.data["tasks"]) > 100:
            self.data["tasks"] = self.data["tasks"][-100:]
        if score:
            self.data["scores"].append(score)
        self.save()

    def add_pattern(self, p):
        if p not in self.data["patterns"]:
            self.data["patterns"].append(p)
            self.save()

    def add_skill(self, s):
        self.data["skills"].append({
            "skill": s,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.data["version"] += 1
        self.save()

    def add_improvement(self, note):
        self.data["improvements"].append({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "note": note[:200]
        })
        self.save()

    def get_context(self):
        p = self.data["patterns"][-5:]
        s = [x["skill"] for x in self.data["skills"][-3:]]
        scores = self.data["scores"][-10:]
        avg = round(sum(scores)/len(scores),1) if scores else 0
        return f"""Tasks done: {len(self.data['tasks'])} | Avg score: {avg}/10
Patterns: {'; '.join(p) if p else 'Building...'}
New skills: {'; '.join(s) if s else 'Learning...'}"""

    @property
    def count(self):
        return len(self.data["tasks"])

    @property
    def version(self):
        return self.data["version"]
