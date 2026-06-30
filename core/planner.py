"""
MODULE 4 — TASK PLANNER
Prompt -> Planner -> Subtasks -> Assign agents -> Merge

Breaks a large request into specific subtasks,
each assigned to the right specialized agent.
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

Available agents (use EXACT codes only):
{agent_list}

Big task to break down:
{big_task}

Break this into 3-8 specific subtasks. You MUST follow this
EXACT format for every subtask, with no extra text, no markdown,
no bullet points — just plain lines exactly like this:

AGENT: CODE
SUBTASK: specific actionable task description
ORDER: 1

AGENT: CODE
SUBTASK: specific actionable task description
ORDER: 2

Rules:
- AGENT must be ONE exact code from the list above (e.g. SALES, CTO, CONT)
- Do not invent new agent codes
- Do not add explanations, headers, or extra commentary
- Only output the AGENT/SUBTASK/ORDER blocks, nothing else
- Order matters: research/architecture before build, build before test/docs"""

        plan_text = self.brain.think(prompt, mode="best")

        print(f"{Fore.WHITE}── Raw planner output ──{Style.RESET_ALL}")
        print(plan_text[:500])
        print(f"{Fore.WHITE}─────────────────────────{Style.RESET_ALL}")

        subtasks = self._parse(plan_text)

        # Fallback: if parsing still fails, retry once with stricter prompt
        if not subtasks:
            print(f"{Fore.YELLOW}⚠️  No subtasks parsed — retrying with strict format...{Style.RESET_ALL}")
            subtasks = self._retry_strict(big_task, agent_list)

        print(f"{Fore.GREEN}✅ Plan ready: {len(subtasks)} subtasks{Style.RESET_ALL}")
        for s in subtasks:
            print(f"  [{s['order']}] {s['agent']}: {s['subtask'][:50]}")

        return subtasks

    def _parse(self, plan_text):
        """Parse AGENT/SUBTASK/ORDER blocks from LLM output"""
        subtasks = []
        lines = plan_text.split("\n")
        current = {}

        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                continue

            upper_line = line.upper()

            if upper_line.startswith("AGENT:"):
                # save previous block if complete
                if current.get("agent") and current.get("subtask"):
                    subtasks.append(current)
                agent_value = line.split(":", 1)[1].strip() if ":" in line else ""
                # clean common formatting noise (markdown, brackets, etc)
                agent_value = (agent_value
                               .replace("*", "")
                               .replace("[", "")
                               .replace("]", "")
                               .strip()
                               .upper())
                current = {"agent": agent_value}

            elif upper_line.startswith("SUBTASK:"):
                subtask_value = line.split(":", 1)[1].strip() if ":" in line else ""
                current["subtask"] = subtask_value

            elif upper_line.startswith("ORDER:"):
                digits = ''.join(c for c in line if c.isdigit())
                try:
                    current["order"] = int(digits) if digits else len(subtasks) + 1
                except:
                    current["order"] = len(subtasks) + 1

        # catch last block
        if current.get("agent") and current.get("subtask"):
            subtasks.append(current)

        # validate agent codes exist in DNA
        valid = []
        for i, s in enumerate(subtasks):
            agent_code = s.get("agent", "").strip()

            if agent_code in DNA:
                s.setdefault("order", i + 1)
                valid.append(s)
            else:
                # try fuzzy match (in case of partial/extra text)
                matched = self._fuzzy_match(agent_code)
                if matched:
                    s["agent"] = matched
                    s.setdefault("order", i + 1)
                    valid.append(s)
                else:
                    print(f"{Fore.RED}⚠️  Unknown agent code skipped: "
                          f"'{agent_code}'{Style.RESET_ALL}")

        return sorted(valid, key=lambda x: x["order"])

    def _fuzzy_match(self, agent_code):
        """Try to match a messy agent code to a real DNA key"""
        if not agent_code:
            return None
        for code in DNA:
            if code in agent_code or agent_code in code:
                return code
        return None

    def _retry_strict(self, big_task, agent_list):
        """One retry with an even simpler, stricter format"""
        prompt = f"""List 4 agents needed for this task: {big_task}

Available codes: {', '.join(DNA.keys())}

Reply with ONLY 4 lines in this exact format, nothing else:
CODE | task description here
CODE | task description here
CODE | task description here
CODE | task description here"""

        result = self.brain.think(prompt, mode="fast")
        subtasks = []

        for i, line in enumerate(result.split("\n")):
            line = line.strip()
            if "|" in line:
                parts = line.split("|", 1)
                code = parts[0].strip().upper()
                task = parts[1].strip() if len(parts) > 1 else big_task

                if code in DNA:
                    subtasks.append({
                        "agent": code,
                        "subtask": task,
                        "order": i + 1
                    })

        return subtasks
