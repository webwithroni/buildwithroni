"""
MODULE 7 — MEMORY UPGRADE
Working Memory / Task Memory / Knowledge Memory /
Learning Memory / Client Memory — instead of one JSON.
"""
import json, os
from datetime import datetime

MEM_DIR = "knowledge/agents"

class MemoryRouter:
    """
    Routes different memory types into separate
    structured stores per agent.
    """

    def __init__(self, agent_code):
        self.code = agent_code
        self.path = f"{MEM_DIR}/{agent_code}_memory.json"
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                return json.load(f)
        return {
            "working_memory":   [],  # current session context
            "task_memory":      [],  # completed tasks log
            "knowledge_memory": [],  # facts learned
            "learning_memory":  [],  # lessons/improvements
            "client_memory":    {},  # per-client context
        }

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_working(self, item):
        self.data["working_memory"].append(item)
        self.data["working_memory"] = self.data["working_memory"][-10:]
        self.save()

    def add_task(self, task, result, score=None):
        self.data["task_memory"].append({
            "time": datetime.now().isoformat(),
            "task": task[:200],
            "result": result[:300],
            "score": score
        })
        self.data["task_memory"] = self.data["task_memory"][-100:]
        self.save()

    def add_knowledge(self, fact, source=""):
        self.data["knowledge_memory"].append({
            "fact": fact, "source": source,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.save()

    def add_lesson(self, lesson):
        self.data["learning_memory"].append({
            "lesson": lesson,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        self.save()

    def update_client(self, client_name, info):
        if client_name not in self.data["client_memory"]:
            self.data["client_memory"][client_name] = {}
        self.data["client_memory"][client_name].update(info)
        self.data["client_memory"][client_name]["last_updated"] = \
            datetime.now().isoformat()
        self.save()

    def get_client(self, client_name):
        return self.data["client_memory"].get(client_name, {})

    def full_context(self):
        return f"""Working Memory: {len(self.data['working_memory'])} items
Tasks Completed: {len(self.data['task_memory'])}
Knowledge Facts: {len(self.data['knowledge_memory'])}
Lessons Learned: {len(self.data['learning_memory'])}
Known Clients: {len(self.data['client_memory'])}"""
