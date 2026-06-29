"""
DEPARTMENT HEAD ENGINE
Senior officials manage their teams.
They break tasks, delegate, collect,
and synthesize results.
"""
from colorama import Fore, Style
from agents.base_agent import Agent, get_brain
from core.agent_dna import DNA

class DepartmentHead:
    """
    A senior official who:
    1. Receives a goal from COA or Roni
    2. Breaks it into agent tasks
    3. Calls the right agents
    4. Synthesizes all results
    5. Reports back a unified answer
    """

    def __init__(self, head_key, team_keys):
        self.head_key = head_key
        self.head = Agent(head_key)
        self.team = {k: Agent(k) for k in team_keys}
        self.brain = get_brain()
        self.dna = DNA[head_key]

    def run(self, goal, auto_delegate=True):
        """
        Full department execution.
        Head plans → agents execute → head synthesizes.
        """
        print(f"\n{Fore.MAGENTA}{'═'*55}")
        print(f"  🏢 {self.dna['name']}")
        print(f"  Department: {self.dna['dept']}")
        print(f"  Goal: {goal[:60]}...")
        print(f"{'═'*55}{Style.RESET_ALL}")

        # Step 1: Head creates execution plan
        plan = self._create_plan(goal)
        print(f"\n{Fore.YELLOW}📋 Execution plan ready{Style.RESET_ALL}")

        if not auto_delegate:
            return plan

        # Step 2: Delegate to agents
        results = self._delegate(goal, plan)

        # Step 3: Synthesize all results
        final = self._synthesize(goal, results)

        return final

    def _create_plan(self, goal):
        """Head creates delegation plan"""
        team_list = "\n".join([
            f"- {k}: {DNA[k]['name']} — {DNA[k]['core']}"
            for k in self.team.keys()
        ])

        prompt = f"""You are {self.dna['name']} at Web With Roni Private Limited.
You are the department head. You must delegate work to your team.

Your team:
{team_list}

Goal assigned to your department:
{goal}

Create a delegation plan. For each relevant team member, write:
AGENT: [code]
TASK: [specific task for this agent]

Only assign agents that are relevant to this goal.
Be specific about what each agent should produce."""

        return self.head.brain.think(prompt, mode="best")

    def _delegate(self, goal, plan):
        """Parse plan and call each agent"""
        results = {}
        lines = plan.split("\n")

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith("AGENT:"):
                agent_code = line.replace("AGENT:","").strip().upper()

                # Get task for this agent
                task = goal  # default
                if i+1 < len(lines):
                    next_line = lines[i+1].strip()
                    if next_line.startswith("TASK:"):
                        task = next_line.replace("TASK:","").strip()
                        i += 1

                # Call the agent if in team
                if agent_code in self.team:
                    print(f"\n{Fore.CYAN}→ Calling {agent_code}: "
                          f"{DNA[agent_code]['name']}{Style.RESET_ALL}")
                    result = self.team[agent_code].think(task)
                    results[agent_code] = {
                        "agent": DNA[agent_code]["name"],
                        "task": task,
                        "result": result
                    }
                    print(f"{Fore.GREEN}  ✅ {agent_code} done{Style.RESET_ALL}")
            i += 1

        # If no agents were parsed, call top 3 relevant agents
        if not results:
            print(f"{Fore.YELLOW}⚡ Auto-selecting agents...{Style.RESET_ALL}")
            for code in list(self.team.keys())[:3]:
                print(f"\n{Fore.CYAN}→ Calling {code}: "
                      f"{DNA[code]['name']}{Style.RESET_ALL}")
                result = self.team[code].think(goal)
                results[code] = {
                    "agent": DNA[code]["name"],
                    "task": goal,
                    "result": result
                }
                print(f"{Fore.GREEN}  ✅ {code} done{Style.RESET_ALL}")

        return results

    def _synthesize(self, goal, results):
        """Head synthesizes all agent results"""
        if not results:
            return "No agent results to synthesize."

        combined = "\n\n".join([
            f"[{v['agent']}]:\n{v['result'][:600]}"
            for k, v in results.items()
        ])

        prompt = f"""You are {self.dna['name']} at Web With Roni Private Limited.
Your team completed their tasks. Now synthesize everything
into ONE comprehensive department report for Roni.

Original goal: {goal}

Team outputs:
{combined}

Write a unified, professional department report.
Include: key findings, recommendations, action items.
Format clearly with sections."""

        print(f"\n{Fore.MAGENTA}🔀 {self.dna['name']} synthesizing...{Style.RESET_ALL}")
        return self.head.brain.think(prompt, mode="ensemble")

    def quick_ask(self, agent_code, task):
        """Directly ask a specific team agent"""
        if agent_code not in self.team:
            return f"Agent {agent_code} not in this department."
        print(f"\n{Fore.CYAN}→ {DNA[agent_code]['name']} working...{Style.RESET_ALL}")
        return self.team[agent_code].think(task)

    def team_status(self):
        """Show all team members status"""
        print(f"\n{Fore.CYAN}{self.dna['dept']} Department{Style.RESET_ALL}")
        print(f"Head: {self.dna['name']}")
        print(f"{'─'*50}")
        for code, agent in self.team.items():
            s = agent.status()
            print(f"  [{code:<6}] {s['name']:<30} "
                  f"v{s['version']} | "
                  f"{s['tasks']} tasks | "
                  f"{s['skills']} skills")
