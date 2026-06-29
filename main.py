#!/usr/bin/env python3
import sys
from colorama import Fore, Style, init
from dotenv import load_dotenv
from agents.base_agent import Agent, get_brain
from core.agent_dna import DNA, DEPARTMENTS

load_dotenv()
init(autoreset=True)

def banner():
    total = sum(len(v) for v in DEPARTMENTS.values())
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
║                                                  ║
║   ⚡  WEB WITH RONI PRIVATE LIMITED              ║
║   AI Command Center v2.0                         ║
║                                                  ║
║   1 Founder · {total} Self-Evolving AI Agents       ║
║   Groq · Mistral · Cerebras Ensemble             ║
║                                                  ║
╚══════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

def load_team():
    print(f"{Fore.YELLOW}⚡ Loading AI Team...{Style.RESET_ALL}\n")
    agents = {}
    for dept, keys in DEPARTMENTS.items():
        for k in keys:
            agents[k] = Agent(k)
        print(f"{Fore.GREEN}✅ {dept:<15} {len(keys)} agents{Style.RESET_ALL}")
    total = len(agents)
    print(f"\n{Fore.CYAN}🚀 {total} agents ready!{Style.RESET_ALL}")
    return agents

def show_team(agents):
    print(f"\n{Fore.WHITE}{'═'*58}")
    print(f"  {'CODE':<8} {'AGENT NAME':<35} {'VER':<5} {'TASKS':<6} SKILLS")
    print(f"{'═'*58}{Style.RESET_ALL}")
    for dept, keys in DEPARTMENTS.items():
        print(f"\n  {Fore.CYAN}{dept.upper()}{Style.RESET_ALL}")
        for k in keys:
            s = agents[k].status()
            print(f"  [{k:<6}] {s['name']:<35} "
                  f"v{s['version']:<4} "
                  f"{s['tasks']:<6} "
                  f"{s['skills']}")

def assign(agents):
    all_keys = [k for keys in DEPARTMENTS.values() for k in keys]

    print(f"\n{Fore.WHITE}{'─'*50}")
    for dept, keys in DEPARTMENTS.items():
        print(f"\n  {Fore.CYAN}{dept}{Style.RESET_ALL}")
        for k in keys:
            print(f"  [{k:<6}] {DNA[k]['name']}")

    choice = input(
        f"\n{Fore.CYAN}Enter agent code (e.g. PROP, FE, COA): {Style.RESET_ALL}"
    ).strip().upper()

    if choice not in agents:
        print(f"{Fore.RED}❌ Agent '{choice}' not found.{Style.RESET_ALL}")
        return

    print(f"\n{Fore.GREEN}✅ {DNA[choice]['name']} selected{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Department: {DNA[choice]['dept']}")
    print(f"Mission: {DNA[choice]['core']}{Style.RESET_ALL}")

    task = input(
        f"\n{Fore.CYAN}Your task: {Style.RESET_ALL}"
    ).strip()

    if not task:
        print(f"{Fore.RED}No task entered.{Style.RESET_ALL}")
        return

    result = agents[choice].think(task)

    print(f"\n{Fore.GREEN}{'═'*55}")
    print(f"  {DNA[choice]['name']} RESPONSE")
    print(f"{'═'*55}{Style.RESET_ALL}")
    print(result)
    print(f"{Fore.GREEN}{'═'*55}{Style.RESET_ALL}")

    # Save to file option
    save = input(
        f"\n{Fore.YELLOW}Save response to file? (y/n): {Style.RESET_ALL}"
    ).strip().lower()
    if save == "y":
        from datetime import datetime
        fname = f"data/{choice}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        os.makedirs("data", exist_ok=True)
        with open(fname, "w") as f:
            f.write(f"Agent: {DNA[choice]['name']}\n")
            f.write(f"Task: {task}\n\n")
            f.write(result)
        print(f"{Fore.GREEN}✅ Saved to {fname}{Style.RESET_ALL}")

def stats(agents):
    brain = get_brain()
    total_tasks  = sum(a.kb.count for a in agents.values())
    total_skills = sum(len(a.dna["skills"]) for a in agents.values())
    total_upgrades = sum(
        len(a.kb.data["skills"]) for a in agents.values()
    )
    print(f"""
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  WEB WITH RONI — TEAM INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Total Agents:      {len(agents)}
  AI Models Active:  {brain.online_count}
  Tasks Completed:   {total_tasks}
  Total Skills:      {total_skills}
  Self-Upgrades:     {total_upgrades}
  Monthly Cost:      $0.00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}""")

import os

def main():
    banner()
    agents = load_team()

    while True:
        print(f"""
{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  COMMAND CENTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [1] Assign task to agent
  [2] View full team roster
  [3] Team intelligence stats
  [0] Exit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}""")

        c = input(f"{Fore.CYAN}Roni → {Style.RESET_ALL}").strip()

        if c == "0":
            print(f"\n{Fore.YELLOW}Team never sleeps. "
                  f"Goodbye Roni! 🚀{Style.RESET_ALL}\n")
            break
        elif c == "1":
            assign(agents)
        elif c == "2":
            show_team(agents)
        elif c == "3":
            stats(agents)
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
