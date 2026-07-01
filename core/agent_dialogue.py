"""
V7 — AGENT-TO-AGENT CONVERSATIONS
Agents ask each other questions instead of
working in isolation.

VISIBLE in terminal by default (Roni sees the
reasoning chain). Set show=False to run silently.

Example flow:
Business: "Need marketing input"
Marketing: "Need competitor data first"
Research: "Here's what I found"
Finance: "Budget concern flagged"
COA: "Approved with conditions"
"""
from colorama import Fore, Style
from core.agent_dna import DNA

class AgentDialogue:

    def __init__(self, brain, show=True):
        self.brain = brain
        self.show = show
        self.conversation_log = []

    def consult(self, task, asking_agent_name, context=""):
        """
        The asking agent identifies who to consult,
        asks them, and gets a real answer back.
        """
        # Step 1: Determine who should be consulted
        agent_list = "\n".join([
            f"{code}: {DNA[code]['name']}" for code in DNA
        ])
        who_prompt = f"""You are {asking_agent_name}. You're working on:
{task[:200]}

Context/concerns: {context[:200]}

Should you consult ANOTHER specialist before finalizing?
If yes, name ONE agent code from this list who'd be most
useful to ask. If no consultation needed, say "NONE".

Available: {', '.join(DNA.keys())}

Reply with just the agent code or NONE."""

        who = self.brain.think(who_prompt, mode="fast").strip().upper()
        who = ''.join(c for c in who if c.isalpha())

        # Find valid match
        target_code = None
        for code in DNA:
            if code in who:
                target_code = code
                break

        if not target_code or target_code == asking_agent_name:
            return "No consultation needed — proceeding independently."

        # Step 2: Ask the question
        question_prompt = f"""You are {asking_agent_name} working on:
{task[:200]}
Concern: {context[:200]}

Write ONE specific question to ask {DNA[target_code]['name']}
({DNA[target_code]['core']}). Keep it to 1-2 sentences."""

        question = self.brain.think(question_prompt, mode="fast")

        if self.show:
            print(f"{Fore.YELLOW}  💬 {asking_agent_name} → "
                  f"{DNA[target_code]['name']}: "
                  f"{question[:80]}{Style.RESET_ALL}")

        # Step 3: Target agent answers
        from agents.base_agent import Agent
        target = Agent(target_code)
        answer = target.think(
            f"{DNA[asking_agent_name] if asking_agent_name in DNA else asking_agent_name} "
            f"is asking you: {question}\n"
            f"Context: working on '{task[:150]}'. "
            f"Give a direct, brief, useful answer (2-3 sentences).",
            use_web=False
        )

        if self.show:
            print(f"{Fore.GREEN}  💬 {DNA[target_code]['name']} → "
                  f"{asking_agent_name}: "
                  f"{answer[:80]}{Style.RESET_ALL}")

        self.conversation_log.append({
            "from": asking_agent_name,
            "to": DNA[target_code]["name"],
            "question": question,
            "answer": answer
        })

        return f"Consulted {DNA[target_code]['name']}: {answer}"

    def multi_agent_chain(self, topic, chain_codes: list):
        """
        Run an explicit conversation chain across multiple
        agents, each responding to the previous one.
        Example: Business -> Marketing -> Research -> Finance -> COA
        """
        print(f"\n{Fore.MAGENTA}🤝 Agent Conversation Chain: "
              f"{topic[:40]}...{Style.RESET_ALL}")

        from agents.base_agent import Agent
        thread = f"Topic: {topic}\n"
        exchanges = []

        for i, code in enumerate(chain_codes):
            agent = Agent(code)
            role_note = "Start the discussion" if i == 0 else \
                        "Respond to the discussion so far"

            response = agent.think(
                f"{role_note} on this topic:\n{thread}\n\n"
                f"Give your perspective in 2-3 sentences as "
                f"{DNA[code]['name']}.", use_web=False
            )

            if self.show:
                print(f"{Fore.CYAN}  🗣️  {DNA[code]['name']}: "
                      f"{response[:100]}{Style.RESET_ALL}")

            thread += f"\n[{DNA[code]['name']}]: {response}"
            exchanges.append({"agent": DNA[code]["name"], "said": response})

        return exchanges, thread
