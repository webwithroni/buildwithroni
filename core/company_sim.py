"""
V6 — COMPANY SIMULATION
Real company hierarchy, not a flat agent list.

CEO (Roni) -> Department Head -> Senior Agent ->
Junior Agent -> QA Agent -> Department Report -> COA
"""
from colorama import Fore, Style
from agents.base_agent import Agent
from core.agent_dna import DNA, DEPARTMENTS
from core.qa import QAEngine

# Seniority tiers within each department
# Head = department leader, Senior = experienced doer,
# Junior = supporting execution
SENIORITY = {
    "Executive":   {"head": "COA", "senior": ["CTO","CGA"], "junior": ["CFA","CLA"]},
    "Business":    {"head": "SALES", "senior": ["PROP","CRM"], "junior": ["LEAD","FLUP"]},
    "Marketing":   {"head": "ANA", "senior": ["SEO","CONT"], "junior": ["FB","IG","LI","EMAIL"]},
    "Creative":    {"head": "BRAND", "senior": ["UI","UX"], "junior": ["GFX","VID"]},
    "Engineering": {"head": "CTO", "senior": ["BE","FE"], "junior": ["MOB","AIB","API","CR","TEST","DOC"]},
    "Support":     {"head": "SUP", "senior": ["TKT"], "junior": ["FAQ","REV"]},
    "Finance":     {"head": "BOOK", "senior": ["INV"], "junior": ["EXP","PAY"]},
}

class CompanySimulation:
    """
    Runs a task through the real company chain of command.
    """

    def __init__(self, brain):
        self.brain = brain
        self.qa = QAEngine(brain)

    def run_department(self, dept_name, task):
        """
        Full department chain:
        Head creates plan -> Senior executes core work ->
        Junior supports -> QA reviews -> Head compiles report
        """
        tiers = SENIORITY.get(dept_name)
        if not tiers:
            return f"Department '{dept_name}' not found."

        print(f"\n{Fore.MAGENTA}🏢 {dept_name} Department — "
              f"Company Simulation{Style.RESET_ALL}")

        head_code = tiers["head"]
        head = Agent(head_code)

        # 1. Head creates delegation plan
        print(f"{Fore.CYAN}  👑 {DNA[head_code]['name']} "
              f"(Head) planning...{Style.RESET_ALL}")
        plan = head.think(
            f"As department head, break this task into 2 parts: "
            f"one for a SENIOR specialist and one for a JUNIOR "
            f"specialist to execute.\nTask: {task}"
        )

        # 2. Senior agent executes core work
        senior_code = tiers["senior"][0]
        senior = Agent(senior_code)
        print(f"{Fore.YELLOW}  🧑‍💼 {DNA[senior_code]['name']} "
              f"(Senior) executing core work...{Style.RESET_ALL}")
        senior_work = senior.think(
            f"As senior specialist, handle the core execution of: "
            f"{task}\nDepartment plan: {plan[:200]}"
        )

        # 3. Junior agent supports
        junior_code = tiers["junior"][0]
        junior = Agent(junior_code)
        print(f"{Fore.WHITE}  🧑‍🎓 {DNA[junior_code]['name']} "
              f"(Junior) supporting...{Style.RESET_ALL}")
        junior_work = junior.think(
            f"As junior specialist, provide supporting work "
            f"(details, examples, checklist) for: {task}\n"
            f"Senior's core work: {senior_work[:200]}"
        )

        # 4. QA reviews before it goes to head
        combined_work = f"{senior_work}\n\n{junior_work}"
        qa_result = self.qa.review(task, combined_work)

        # 5. Head compiles final department report
        print(f"{Fore.CYAN}  👑 {DNA[head_code]['name']} "
              f"compiling department report...{Style.RESET_ALL}")
        report = head.think(
            f"Compile the final department report from your team's work.\n"
            f"Original task: {task}\n"
            f"Senior work: {senior_work[:400]}\n"
            f"Junior support: {junior_work[:300]}\n"
            f"QA notes: {qa_result['review'][:200]}\n"
            f"Write ONE unified, polished department report."
        )

        print(f"{Fore.GREEN}  ✅ {dept_name} department report ready "
              f"(QA: {'PASS' if qa_result['passed'] else 'FLAGGED'})"
              f"{Style.RESET_ALL}")

        return {
            "department": dept_name,
            "head": DNA[head_code]["name"],
            "senior_work": senior_work,
            "junior_work": junior_work,
            "qa_passed": qa_result["passed"],
            "report": report
        }

    def full_company(self, ceo_task):
        """
        CEO task -> relevant departments run in simulation ->
        COA compiles company-wide report
        """
        print(f"\n{Fore.MAGENTA}{'═'*55}")
        print(f"  🏢 FULL COMPANY SIMULATION")
        print(f"  CEO Task: {ceo_task[:50]}...")
        print(f"{'═'*55}{Style.RESET_ALL}")

        coa = Agent("COA")
        route_prompt = f"""As COA, which 2-3 departments should
handle this task? Available: {', '.join(SENIORITY.keys())}
Task: {ceo_task}
Reply with just department names, one per line."""

        routing = coa.think(route_prompt)
        depts_to_run = [
            d for d in SENIORITY.keys()
            if d.lower() in routing.lower()
        ][:3] or list(SENIORITY.keys())[:2]

        dept_reports = {}
        for dept in depts_to_run:
            dept_reports[dept] = self.run_department(dept, ceo_task)

        combined = "\n\n".join([
            f"[{d} DEPARTMENT — Head: {r['head']}]\n{r['report'][:400]}"
            for d, r in dept_reports.items()
        ])

        final = coa.think(
            f"Compile the FINAL COMPANY REPORT from all department "
            f"reports for Roni (CEO).\nOriginal task: {ceo_task}\n"
            f"Department reports:\n{combined}"
        )

        return final
