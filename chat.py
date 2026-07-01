#!/usr/bin/env python3
"""
WEB WITH RONI PRIVATE LIMITED
Unified AI Chat Interface v4.0 — Project Titan
Enterprise-grade AI consulting terminal.
"""
import os
from colorama import Fore, Style, init
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

from agents.base_agent import Agent, get_brain, get_web
from core.auto_router import AutoRouter
from core.workflow import Workflow
from core.agent_dna import DNA

# ═══════════════════════════════════════════
# MASTER SYSTEM PROMPT — WHO WE ARE
# ═══════════════════════════════════════════
SYSTEM_PROMPT = """
You are the Chief Operating Intelligence of
Web With Roni Private Limited.

Act as a team of specialized experts including:
CEO Advisor, CTO, Solution Architect,
Product Manager, UI/UX Designer,
Senior Full-Stack Engineer, AI Engineer,
DevOps Engineer, QA Lead, Growth Strategist,
Marketing Director, Legal Advisor,
Finance Advisor, HR Manager,
Cybersecurity Expert, and Customer Success Manager.

Always think like an enterprise IT consulting company.

Prioritize:
- Scalable architecture
- Clean code
- Security
- Automation
- Maintainability
- Performance
- Business value

Recommend AI-first solutions whenever appropriate.

Before answering ALWAYS:
1. Clarify the business objective
2. Analyze technical constraints
3. Recommend optimal architecture
4. Explain trade-offs
5. Provide production-ready solutions
6. Suggest automation opportunities
7. Consider cost, scalability, security, future growth

Treat every conversation as if you are helping
build a world-class AI-native IT company.
Maintain documentation, consistency, and
reusable processes across the project.

Company: Web With Roni Private Limited
Founder: Roni
Model: 1 human + 38 AI agents
Stack: Termux, Python, GitHub, Vercel
"""

def banner():
    print(f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   ⚡  WEB WITH RONI PRIVATE LIMITED                  ║
║   Enterprise AI Chat — Project Titan v4.0            ║
║                                                      ║
║   Chief Operating Intelligence — Online              ║
║   38 Agents · 3 AI Models · Real-time Web            ║
║                                                      ║
║   Commands:                                          ║
║   'team'   → Show all 38 agents                      ║
║   'status' → System health check                     ║
║   'save'   → Save last response                      ║
║   'clear'  → Clear screen                            ║
║   'exit'   → Shutdown                                ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

def boot():
    print(f"{Fore.YELLOW}⚡ Initializing enterprise AI system...{Style.RESET_ALL}\n")
    brain = get_brain()
    web   = get_web()
    router   = AutoRouter(brain)
    workflow = Workflow()
    print(f"\n{Fore.GREEN}✅ System ready. How can I help, Roni?{Style.RESET_ALL}\n")
    return brain, web, router, workflow

def handle(user_prompt, router, workflow, brain):
    """
    Core routing engine.
    Every prompt goes through system context
    then routes to best agent or full workflow.
    """
    # Inject system context into every request
    enriched_prompt = f"{SYSTEM_PROMPT}\n\nRONI'S REQUEST:\n{user_prompt}"

    print(f"\n{Fore.YELLOW}🧠 Analyzing request...{Style.RESET_ALL}")
    decision = router.classify(user_prompt)

    if decision["complexity"] == "COMPLEX":
        print(f"{Fore.MAGENTA}📋 Strategic task — activating full workflow")
        print(f"   Planner → Debate → QA → Truth Guard → Report")
        print(f"   Reason: {decision['reason']}{Style.RESET_ALL}\n")
        result = workflow.run_full_task(enriched_prompt)
        agent_used = "Full Enterprise Workflow"

    else:
        code = decision["agent"]
        name = DNA.get(code, {}).get("name", "Chief Operating Agent")
        dept = DNA.get(code, {}).get("dept", "")

        print(f"{Fore.CYAN}🤖 Expert: {name} ({code}) — {dept}")
        print(f"   Reason: {decision['reason']}{Style.RESET_ALL}\n")

        agent = Agent(code)
        result = agent.think(enriched_prompt)
        agent_used = f"{name} ({code})"

    return result, agent_used, decision

def show_team():
    from core.agent_dna import DEPARTMENTS
    print(f"\n{Fore.CYAN}{'═'*55}")
    print(f"  WEB WITH RONI — FULL AI TEAM")
    print(f"{'═'*55}{Style.RESET_ALL}")
    for dept, keys in DEPARTMENTS.items():
        print(f"\n  {Fore.YELLOW}{dept}{Style.RESET_ALL}")
        for k in keys:
            d = DNA[k]
            print(f"  [{k:<6}] {d['name']:<35} {d['core'][:25]}")

def show_status(brain, web):
    from core.agent_dna import DEPARTMENTS
    total = sum(len(v) for v in DEPARTMENTS.values())
    print(f"""
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SYSTEM STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AI Models:      {brain.online_count}/5 online
  Search Engines: {len(web.available)}/3 online
  Agents Ready:   {total}
  System Version: Project Titan v4.0
  Monthly Cost:   $0.00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}""")

def save_response(prompt, result, agent_used):
    from datetime import datetime
    os.makedirs("data", exist_ok=True)
    fname = f"data/chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, "w") as f:
        f.write(f"WEB WITH RONI PRIVATE LIMITED\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"PROMPT:\n{prompt}\n\n")
        f.write(f"HANDLED BY: {agent_used}\n\n")
        f.write(f"RESPONSE:\n{result}\n")
    return fname

def main():
    banner()
    brain, web, router, workflow = boot()

    last_result = None
    last_prompt = None
    last_agent  = None

    while True:
        try:
            user_input = input(
                f"{Fore.CYAN}Roni → {Style.RESET_ALL}"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{Fore.YELLOW}Goodbye Roni! 🚀{Style.RESET_ALL}\n")
            break

        if not user_input:
            continue

        # ── Built-in commands ──
        if user_input.lower() == "exit":
            print(f"\n{Fore.YELLOW}Team never sleeps. "
                  f"Goodbye Roni! 🚀{Style.RESET_ALL}\n")
            break

        elif user_input.lower() == "team":
            show_team()
            continue

        elif user_input.lower() == "status":
            show_status(brain, web)
            continue

        elif user_input.lower() == "clear":
            os.system("clear")
            banner()
            continue

        elif user_input.lower() == "save":
            if last_result:
                fname = save_response(
                    last_prompt, last_result, last_agent
                )
                print(f"{Fore.GREEN}💾 Saved → {fname}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Nothing to save yet.{Style.RESET_ALL}")
            continue

        # ── Main AI processing ──
        try:
            result, agent_used, decision = handle(
                user_input, router, workflow, brain
            )

            # Display result
            print(f"\n{Fore.GREEN}{'═'*58}")
            print(f"  {agent_used}")
            print(f"{'═'*58}{Style.RESET_ALL}")
            print(result)
            print(f"{Fore.GREEN}{'═'*58}{Style.RESET_ALL}")

            # Store for save command
            last_result = result
            last_prompt = user_input
            last_agent  = agent_used

            # Auto-save complex results
            if decision["complexity"] == "COMPLEX":
                fname = save_response(user_input, result, agent_used)
                print(f"\n{Fore.GREEN}💾 Auto-saved → {fname}{Style.RESET_ALL}")

        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Try rephrasing. "
                  f"Team is still online.{Style.RESET_ALL}")

        print()

if __name__ == "__main__":
    main()
