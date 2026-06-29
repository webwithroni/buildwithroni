from colorama import Fore, Style

class SelfLearner:
    def __init__(self, code, brain):
        self.code = code
        self.brain = brain

    def score(self, task, response, role):
        prompt = f"""You are {role}. Score your own response 1-10.
Task: {task[:150]}
Response: {response[:300]}
Reply with ONLY a single number 1-10. Nothing else."""
        try:
            r = self.brain.think(prompt, mode="fast")
            n = ''.join(c for c in r.strip() if c.isdigit() or c == '.')[:3]
            return min(max(float(n), 1.0), 10.0)
        except:
            return 7.0

    def extract_patterns(self, task, response):
        prompt = f"""Extract 2-3 reusable work patterns from this:
Task: {task[:100]}
Response: {response[:200]}
Return ONLY 2-3 short phrases, one per line. No numbering."""
        try:
            r = self.brain.think(prompt, mode="fast")
            return [l.strip() for l in r.strip().split("\n")
                    if l.strip() and len(l.strip()) > 8][:3]
        except:
            return []

    def improve(self, role, tasks):
        if len(tasks) < 3:
            return ""
        summary = "\n".join([
            f"- {t['task'][:60]} | Score: {t.get('score','?')}"
            for t in tasks[-8:]
        ])
        prompt = f"""You are {role}. Review your recent work:
{summary}
Write 3 specific one-sentence improvements. Plain list only."""
        try:
            return self.brain.think(prompt, mode="fast")
        except:
            return ""

    def new_skill(self, role, skills):
        prompt = f"""You are {role}.
Current skills: {', '.join(skills[:5])}
Identify ONE new valuable skill to learn.
Format: SKILL: [name]
Then 1 sentence why it helps Web With Roni."""
        try:
            r = self.brain.think(prompt, mode="fast")
            for line in r.split("\n"):
                if "SKILL:" in line:
                    return line.replace("SKILL:","").strip()
            return "Advanced specialization"
        except:
            return "Advanced specialization"
