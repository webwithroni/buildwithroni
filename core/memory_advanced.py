"""
ADVANCED MEMORY SYSTEM
Layered like real human memory:
Short-term (session) / Working (active task) /
Long-term (persistent facts) / Episodic (events/history) /
Semantic (learned concepts)
"""
import json, os
from datetime import datetime

MEM_DIR = "knowledge/advanced_memory"
os.makedirs(MEM_DIR, exist_ok=True)

class AdvancedMemory:
    def __init__(self, agent_code):
        self.code = agent_code
        self.path = f"{MEM_DIR}/{agent_code}.json"
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {
            "short_term": [],     # last N interactions (volatile)
            "working": {},        # current active task context
            "long_term": [],      # durable facts about company/clients
            "episodic": [],       # significant events with timestamps
            "semantic": {}        # concept -> understanding, grows over time
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def remember_short(self, item):
        self.data["short_term"].append({"t": datetime.now().isoformat(), "item": item})
        self.data["short_term"] = self.data["short_term"][-15:]
        self.save()

    def set_working(self, key, value):
        self.data["working"][key] = value
        self.save()

    def remember_long(self, fact, importance="normal"):
        self.data["long_term"].append({
            "fact": fact, "importance": importance,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.save()

    def log_episode(self, event, outcome=""):
        self.data["episodic"].append({
            "t": datetime.now().isoformat(),
            "event": event, "outcome": outcome
        })
        self.data["episodic"] = self.data["episodic"][-100:]
        self.save()

    def learn_concept(self, concept, understanding):
        existing = self.data["semantic"].get(concept, "")
        merged = f"{existing} | {understanding}" if existing else understanding
        self.data["semantic"][concept] = merged[:500]
        self.save()

    def full_context(self, max_chars=800):
        st = "; ".join(i["item"] for i in self.data["short_term"][-5:])
        lt = "; ".join(f["fact"] for f in self.data["long_term"][-5:])
        ep = "; ".join(f"{e['event']}→{e['outcome']}" for e in self.data["episodic"][-3:])
        sem = "; ".join(f"{k}: {v[:60]}" for k, v in list(self.data["semantic"].items())[-5:])
        block = (f"Recent: {st}\nKey facts: {lt}\n"
                 f"Recent events: {ep}\nUnderstood concepts: {sem}")
        return block[:max_chars]
