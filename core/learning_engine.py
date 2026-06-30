"""
MODULE 10 — LEARNING ENGINE
Task -> Review -> Score -> Mistakes -> Lessons ->
Knowledge Base -> Skill Improvement
"""
from colorama import Fore, Style

class LearningEngine:

    def __init__(self, brain, memory_router):
        self.brain = brain
        self.mem = memory_router

    def process(self, task, response, qa_review):
        """Full learning cycle after task completion"""
        print(f"{Fore.YELLOW}📖 Learning Engine processing...{Style.RESET_ALL}")

        mistakes = self._find_mistakes(task, response, qa_review)
        lessons = self._extract_lessons(task, response, mistakes)

        for lesson in lessons:
            self.mem.add_lesson(lesson)

        self.mem.add_task(task, response)

        print(f"{Fore.GREEN}✅ {len(lessons)} lessons learned{Style.RESET_ALL}")
        return lessons

    def _find_mistakes(self, task, response, qa_review):
        if qa_review.get("passed"):
            return "No significant mistakes — QA passed."
        return qa_review.get("review", "")

    def _extract_lessons(self, task, response, mistakes):
        prompt = f"""Task: {task[:150]}
Mistakes/Issues found: {mistakes[:300]}

Extract 1-2 specific lessons to remember for next time.
Format: one short lesson per line, no numbering."""

        result = self.brain.think(prompt, mode="fast")
        return [l.strip() for l in result.split("\n")
                if l.strip() and len(l.strip()) > 10][:2]
