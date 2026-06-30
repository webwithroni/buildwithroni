"""
MODULE 4 — TASK PLANNER
Prompt -> Planner -> Subtasks -> Assign agents -> Merge
"""
from colorama import Fore, Style
from core.agent_dna import DNA, DEPARTMENTS

class TaskPlanner:

    def __init__(self, brain):
        self.brain = brain

    def plan(self, big_task: str) -> list:
        """
        Break a large request into subtasks,
        each assigned to the right agent.
        """
        print(f"{Fore.YELLOW}🗺️  Planner breaking down task...{Style.RESET_ALL}")

        agent_list = "\n".join([
            f"{code}: {DNA[code]['name']} — {DNA[code]['core']}"
            for code in DNA
        ])

        prompt = f"""You are the Task Planner at Web With Roni Private Limited.

Available agents:
{agent_list}

Big task to break down:
{big_task}

Break this into 3-10 specific subtasks. For each subtask write:
AGENT: [exact agent code from list above]
SUBTASK: [specific, actionable task]
ORDER: [number — execution order, 1 first]

Only include subtasks genuinely needed. Order matters —
research/architecture before build, build before test/docs."""

        plan_text = self.brain.think(prompt, mode="best")
        subtasks = self._parse(plan_text)

        print(f"{Fore.GREEN}✅ Plan ready: {len(subtasks)} subtasks{Style.RESET_ALL}")
        for s in subtasks:
            print(f"  [{s['order']}] {s['agent']}: {s['subtask'][:50]}")

        return subtasks

    def _parse(self, plan_text):
        subtasks = []
        lines = plan_text.split("\n")
        current = {}

        for line in lines:
            line = line.strip()
            if line.startswith("AGENT:"):
                if current.get("agent") and current.get("subtask"):
                    subtasks.append(current)
                current = {"agent": line.replace("AGENT:","").strip().upper()}
            elif line.startswith("SUBTASK:"):
                current["subtask"] = line.replace("SUBTASK:","").strip()
            elif line.startswith("ORDER:"):
                try:
                    current["order"] = int(
                        ''.join(c for c in line if c.isdigit())
                    )
                except:
                    current["order"] = len(subtasks) + 1

        if current.get("agent") and current.get("subtask"):
            subtasks.append(current)

        # Validate agents exist, default order
        valid = []
        for i, s in enumerate(subtasks):
            if s.get("agent") in DNA:
                s.setdefault("order", i+1)
                valid.append(s)

        return sorted(valid, key=lambda x: x["order"])
