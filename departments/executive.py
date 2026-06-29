from core.department_head import DepartmentHead
from agents.base_agent import Agent, get_brain
from core.agent_dna import DNA, DEPARTMENTS
from colorama import Fore, Style

class ExecutiveTeam:
    """
    COA coordinates all departments.
    CTO leads engineering.
    Other C-suite handle their domains.
    """

    def __init__(self, all_departments):
        self.coa = Agent("COA")
        self.cto = Agent("CTO")
        self.cga = Agent("CGA")
        self.cfa = Agent("CFA")
        self.cla = Agent("CLA")
        self.brain = get_brain()
        self.departments = all_departments

    def full_company_task(self, goal):
        """
        COA receives goal → assigns to departments
        → collects results → final report to Roni
        """
        print(f"\n{Fore.MAGENTA}{'═'*58}")
        print(f"  🧠 COA ORCHESTRATING FULL COMPANY")
        print(f"  Goal: {goal[:55]}...")
        print(f"{'═'*58}{Style.RESET_ALL}")

        # COA creates company-wide plan
        dept_list = "\n".join([
            f"- {name}: {', '.join(keys)}"
            for name, keys in DEPARTMENTS.items()
        ])

        plan_prompt = f"""You are the Chief Operating Agent at Web With Roni Private Limited.
Roni (CEO) has given you this goal:
{goal}

Available departments:
{dept_list}

Decide which departments should work on this goal.
For each relevant department write:
DEPT: [department name]
TASK: [specific task for that department]

Be strategic. Not every goal needs all departments."""

        print(f"\n{Fore.YELLOW}🤔 COA analyzing goal...{Style.RESET_ALL}")
        plan = self.brain.think(plan_prompt, mode="ensemble")
        print(f"{Fore.GREEN}✅ Company plan ready{Style.RESET_ALL}")

        # Parse and execute department tasks
        dept_results = {}
        lines = plan.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("DEPT:"):
                dept_name = line.replace("DEPT:","").strip()
                task = goal
                if i+1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line.startswith("TASK:"):
                        task = next_line.replace("TASK:","").strip()
                        i += 1

                # Find matching department
                for key, dept in self.departments.items():
                    if key.lower() in dept_name.lower() or \
                       dept_name.lower() in key.lower():
                        print(f"\n{Fore.BLUE}🏢 Activating {key} dept...{Style.RESET_ALL}")
                        result = dept.run(task)
                        dept_results[key] = result
                        break
            i += 1

        # If no depts parsed, use top 3
        if not dept_results:
            for key in list(self.departments.keys())[:3]:
                print(f"\n{Fore.BLUE}🏢 Activating {key} dept...{Style.RESET_ALL}")
                result = self.departments[key].run(goal)
                dept_results[key] = result

        # COA final synthesis
        return self._final_report(goal, dept_results)

    def _final_report(self, goal, dept_results):
        combined = "\n\n".join([
            f"[{dept} DEPARTMENT]:\n{result[:500]}"
            for dept, result in dept_results.items()
        ])

        prompt = f"""You are the Chief Operating Agent at Web With Roni Private Limited.
All departments have completed their work.
Compile everything into a FINAL EXECUTIVE REPORT for Roni.

Original goal: {goal}

Department results:
{combined}

Write a clear executive summary with:
1. Executive Summary
2. Key outputs from each department
3. Recommended next actions for Roni
4. Timeline suggestions
Format professionally."""

        print(f"\n{Fore.MAGENTA}📊 COA compiling executive report...{Style.RESET_ALL}")
        return self.brain.think(prompt, mode="ensemble")

    def cto_review(self, technical_item):
        """CTO reviews technical decisions"""
        return self.cto.think(
            f"As CTO, review and advise on: {technical_item}"
        )

    def cga_strategy(self, growth_goal):
        """CGA creates growth strategy"""
        return self.cga.think(
            f"Create growth strategy for: {growth_goal}"
        )

    def cfa_analysis(self, financial_question):
        """CFA analyzes financial matters"""
        return self.cfa.think(
            f"Analyze financially: {financial_question}"
        )

    def cla_review(self, legal_matter):
        """CLA reviews legal matters"""
        return self.cla.think(
            f"Review legally: {legal_matter}"
        )
