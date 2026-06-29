#!/usr/bin/env python3
"""
WEB WITH RONI PRIVATE LIMITED
Full Hierarchical Command Center
Senior Officials → Department Teams → Results
"""
import os, sys
from colorama import Fore, Style, init
from dotenv import load_dotenv

load_dotenv()
init(autoreset=True)

from departments.executive  import ExecutiveTeam
from departments.business   import BusinessDept
from departments.marketing  import MarketingDept
from departments.creative   import CreativeDept
from departments.engineering import EngineeringDept
from departments.support    import SupportDept
from departments.finance    import FinanceDept
from agents.base_agent      import Agent
from core.agent_dna         import DNA, DEPARTMENTS

def banner():
    print(f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   ⚡  WEB WITH RONI PRIVATE LIMITED                  ║
║   Full Hierarchical AI Command Center v3.0           ║
║                                                      ║
║   👤 Roni (CEO) → COA → 7 Depts → 38 Agents         ║
║   Self-Learning · Self-Improving · Self-Upgrading    ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")

def boot():
    print(f"{Fore.YELLOW}⚡ Booting all departments...{Style.RESET_ALL}\n")

    depts = {
        "Business":    BusinessDept(),
        "Marketing":   MarketingDept(),
        "Creative":    CreativeDept(),
        "Engineering": EngineeringDept(),
        "Support":     SupportDept(),
        "Finance":     FinanceDept(),
    }

    exec_team = ExecutiveTeam(depts)

    for name in depts:
        print(f"{Fore.GREEN}✅ {name} Department online{Style.RESET_ALL}")

    print(f"\n{Fore.CYAN}🚀 Full company online! 38 agents ready.{Style.RESET_ALL}")
    return exec_team, depts

def show_menu():
    print(f"""
{Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  👤 RONI COMMAND CENTER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  🧠 EXECUTIVE COMMANDS
  [1]  Full company task (COA orchestrates all)
  [2]  CTO — Technical review / architecture
  [3]  CGA — Growth strategy
  [4]  CFA — Financial analysis
  [5]  CLA — Legal review

  💼 BUSINESS
  [6]  Full client acquisition pipeline
  [7]  Write proposal for client
  [8]  Find leads in niche

  📣 MARKETING
  [9]  Full marketing campaign
  [10] LinkedIn post
  [11] Blog post
  [12] Email campaign

  🎨 CREATIVE
  [13] Full brand identity package
  [14] Design system
  [15] Video script

  💻 ENGINEERING
  [16] Full project build
  [17] Build website
  [18] Code review
  [19] AI system design

  🎧 SUPPORT
  [20] Handle client issue
  [21] Generate FAQs

  💰 FINANCE
  [22] Create invoice
  [23] Expense report

  🤖 DIRECT AGENT
  [24] Talk to any agent directly

  📊 SYSTEM
  [25] Team status
  [0]  Exit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}""")

def save_result(result, label="result"):
    """Auto save every result"""
    from datetime import datetime
    os.makedirs("data", exist_ok=True)
    fname = f"data/{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(fname, "w") as f:
        f.write(result)
    print(f"\n{Fore.GREEN}💾 Saved → {fname}{Style.RESET_ALL}")

def show_result(result, title="RESULT"):
    print(f"\n{Fore.GREEN}{'═'*58}")
    print(f"  {title}")
    print(f"{'═'*58}{Style.RESET_ALL}")
    print(result)
    print(f"{Fore.GREEN}{'═'*58}{Style.RESET_ALL}")

def main():
    banner()
    exec_team, depts = boot()

    while True:
        show_menu()
        choice = input(
            f"{Fore.CYAN}Roni → Choose: {Style.RESET_ALL}"
        ).strip()

        result = None

        if choice == "0":
            print(f"\n{Fore.YELLOW}Your team never sleeps."
                  f" Goodbye Roni! 🚀{Style.RESET_ALL}\n")
            break

        elif choice == "1":
            goal = input("Full company goal: ").strip()
            result = exec_team.full_company_task(goal)

        elif choice == "2":
            item = input("Technical item to review: ").strip()
            result = exec_team.cto_review(item)

        elif choice == "3":
            goal = input("Growth goal: ").strip()
            result = exec_team.cga_strategy(goal)

        elif choice == "4":
            q = input("Financial question: ").strip()
            result = exec_team.cfa_analysis(q)

        elif choice == "5":
            matter = input("Legal matter to review: ").strip()
            result = exec_team.cla_review(matter)

        elif choice == "6":
            target = input("Target client/niche: ").strip()
            result = depts["Business"].get_new_client(target)

        elif choice == "7":
            client = input("Client name & business: ").strip()
            service = input("Service needed: ").strip()
            budget = input("Budget (optional): ").strip()
            result = depts["Business"].write_proposal(
                client, service, budget
            )

        elif choice == "8":
            niche = input("Target niche: ").strip()
            result = depts["Business"].find_leads(niche)

        elif choice == "9":
            topic = input("Campaign topic: ").strip()
            result = depts["Marketing"].full_campaign(topic)

        elif choice == "10":
            topic = input("LinkedIn post topic: ").strip()
            result = depts["Marketing"].linkedin_post(topic)

        elif choice == "11":
            topic = input("Blog post topic: ").strip()
            result = depts["Marketing"].blog_post(topic)

        elif choice == "12":
            target = input("Email target audience: ").strip()
            service = input("Service to pitch: ").strip()
            result = depts["Marketing"].email_sequence(target, service)

        elif choice == "13":
            info = input("Business info for branding: ").strip()
            result = depts["Creative"].full_brand(info)

        elif choice == "14":
            brand = input("Brand to design for: ").strip()
            result = depts["Creative"].design_system(brand)

        elif choice == "15":
            topic = input("Video topic: ").strip()
            dur = input("Duration (30s/60s/2min): ").strip()
            result = depts["Creative"].video_script(topic, dur)

        elif choice == "16":
            desc = input("Project description: ").strip()
            result = depts["Engineering"].build_project(desc)

        elif choice == "17":
            client = input("Client name: ").strip()
            req = input("Website requirements: ").strip()
            result = depts["Engineering"].build_website(client, req)

        elif choice == "18":
            lang = input("Language (Python/JS/HTML): ").strip()
            print("Paste code (type END when done):")
            lines = []
            while True:
                line = input()
                if line.strip() == "END":
                    break
                lines.append(line)
            result = depts["Engineering"].code_review(
                "\n".join(lines), lang
            )

        elif choice == "19":
            desc = input("AI system to build: ").strip()
            result = depts["Engineering"].ai_system(desc)

        elif choice == "20":
            client = input("Client name: ").strip()
            issue = input("Issue description: ").strip()
            result = depts["Support"].handle_issue(client, issue)

        elif choice == "21":
            service = input("Service to create FAQs for: ").strip()
            result = depts["Support"].generate_faqs(service)

        elif choice == "22":
            client = input("Client name: ").strip()
            services = input("Services provided: ").strip()
            amount = input("Total amount: ").strip()
            result = depts["Finance"].create_invoice(
                client, services, amount
            )

        elif choice == "23":
            expenses = input("List your expenses: ").strip()
            result = depts["Finance"].expense_report(expenses)

        elif choice == "24":
            print(f"\n{Fore.WHITE}Agent codes:{Style.RESET_ALL}")
            for dept, keys in DEPARTMENTS.items():
                print(f"  {dept}: {' '.join(keys)}")
            code = input("\nAgent code: ").strip().upper()
            if code in DNA:
                task = input(f"Task for {DNA[code]['name']}: ").strip()
                agent = Agent(code)
                result = agent.think(task)
            else:
                print(f"{Fore.RED}Agent not found.{Style.RESET_ALL}")

        elif choice == "25":
            for name, dept in depts.items():
                dept.team_status()

        if result:
            show_result(result, f"RESULT — {choice}")
            save = input(
                f"\n{Fore.YELLOW}Save? (y/n): {Style.RESET_ALL}"
            ).strip().lower()
            if save == "y":
                save_result(result, f"task_{choice}")

        if choice != "0":
            input(
                f"\n{Fore.YELLOW}Press Enter...{Style.RESET_ALL}"
            )

if __name__ == "__main__":
    main()

# Web Intelligence standalone commands added to menu
def web_search_menu(web):
    print(f"""
{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🌐 WEB INTELLIGENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [w1] Search anything live
  [w2] Latest news on topic
  [w3] Market research
  [w4] Competitor analysis
  [w5] Price check
  [w0] Back
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}""")

    c = input(f"{Fore.CYAN}Web → {Style.RESET_ALL}").strip()

    if c == "w1":
        q = input("Search query: ").strip()
        return web.search(q)
    elif c == "w2":
        t = input("Topic for news: ").strip()
        return web.news(t)
    elif c == "w3":
        i = input("Industry to research: ").strip()
        return web.market(i)
    elif c == "w4":
        co = input("Competitor name: ").strip()
        return web.competitor(co)
    elif c == "w5":
        s = input("Service to price check: ").strip()
        return web.price_check(s)
    return None
