"""
WORKFLOW — FULL EXECUTION FLOW — v2
CEO -> Planner -> Task Split -> Department Heads ->
Agents -> Research -> Debate -> QA -> Truth Guard ->
Executive Merge -> Final Report -> Learning Engine -> Memory
"""
import time
from colorama import Fore, Style
from agents.base_agent import Agent, get_brain, get_web
from core.planner import TaskPlanner
from core.debate import DebateEngine
from core.qa import QAEngine
from core.truth_guard import TruthGuard
from core.memory_router import MemoryRouter
from core.learning_engine import LearningEngine
from core.prompt_compiler import PromptCompiler
from core.agent_dna import DNA

class Workflow:

    def __init__(self):
        self.brain    = get_brain()
        self.web      = get_web()
        self.planner  = TaskPlanner(self.brain)
        self.debate   = DebateEngine(self.brain)
        self.qa       = QAEngine(self.brain)
        self.guard    = TruthGuard(self.brain)

    def run_full_task(self, big_task, run_debate=True):
        print(f"\n{Fore.MAGENTA}{'═'*58}")
        print(f"  🚀 PROJECT TITAN — FULL WORKFLOW")
        print(f"  Task: {big_task[:50]}...")
        print(f"{'═'*58}{Style.RESET_ALL}")

        # 1. PLANNER
        subtasks = self.planner.plan(big_task)

        # 2. DEBATE
        debate_result = None
        if run_debate:
            debate_result = self.debate.debate(big_task)

        # 3. AGENTS EXECUTE subtasks
        agent_results = {}
        for sub in subtasks:
            code = sub["agent"]
            task = sub["subtask"]

            print(f"\n{Fore.CYAN}→ {DNA[code]['name']} "
                  f"executing: {task[:40]}...{Style.RESET_ALL}")

            agent = Agent(code)
            mem   = MemoryRouter(code)

            # Web research
            web_data     = self.web.search(task[:80])
            has_evidence = bool(
                web_data and "No results" not in web_data
            )

            # Compile prompt
            compiler = PromptCompiler(DNA[code], agent.kb, self.web)
            prompt   = compiler.compile(
                task, web_data=web_data,
                output_format="standard"
            )

            # Execute with retry
            response = self._call_with_retry(prompt, DNA[code].get("style","best"))

            if not response:
                print(f"{Fore.RED}⚠️  {code} skipped — all models failed{Style.RESET_ALL}")
                continue

            # QA
            qa_result = self.qa.review(task, response)

            # Truth Guard
            verified, confidence = self.guard.validate(
                response, has_evidence
            )

            # Learning
            learner = LearningEngine(self.brain, mem)
            learner.process(task, response, qa_result)

            agent_results[code] = {
                "agent":      DNA[code]["name"],
                "task":       task,
                "response":   verified,
                "qa_passed":  qa_result["passed"],
                "confidence": confidence["score"]
            }

            # Small pause to avoid rate limit spikes
            time.sleep(0.5)

        # 4. EXECUTIVE MERGE with retry
        final = self._executive_merge_with_retry(
            big_task, agent_results, debate_result
        )
        return final

    def _call_with_retry(self, prompt, mode, max_retries=3):
        """Retry with backoff on model failure"""
        for attempt in range(max_retries):
            result = self.brain.think(prompt, mode=mode)
            if result and "All models failed" not in result:
                return result
            wait = (attempt + 1) * 3
            print(f"{Fore.YELLOW}⚠️  Retry {attempt+1}/{max_retries} "
                  f"in {wait}s...{Style.RESET_ALL}")
            time.sleep(wait)
        return None

    def _executive_merge_with_retry(self, big_task,
                                     agent_results, debate_result):
        """Executive merge with retry on rate limit"""
        combined = "\n\n".join([
            f"[{v['agent']}] "
            f"(Confidence: {v['confidence']}%, "
            f"QA: {'PASS' if v['qa_passed'] else 'FLAGGED'}):\n"
            f"{v['response'][:400]}"
            for v in agent_results.values()
        ])

        debate_section = ""
        if debate_result:
            debate_section = (f"\nDEPARTMENT DEBATE:\n"
                              f"{debate_result['decision'][:500]}")

        prompt = f"""You are the Chief Operating Agent at
Web With Roni Private Limited.

Compile a FINAL EXECUTIVE REPORT for Roni.

Original request: {big_task[:300]}

Agent outputs:
{combined}
{debate_section}

Format EXACTLY as:

EXECUTIVE SUMMARY:

OBJECTIVES:

ANALYSIS:

EVIDENCE:

RISKS:

RECOMMENDATIONS:

KPIS:

ACTION PLAN:

CONFIDENCE:

NEXT STEP:"""

        print(f"\n{Fore.MAGENTA}👑 Executive merging final report...{Style.RESET_ALL}")

        # Wait before final merge to let rate limits recover
        time.sleep(2)

        result = self._call_with_retry(prompt, "ensemble")
        return result or self._fallback_report(big_task, agent_results)

    def _fallback_report(self, big_task, agent_results):
        """If all retries fail, compile from agent results directly"""
        print(f"{Fore.YELLOW}📋 Using fallback report builder...{Style.RESET_ALL}")
        report = f"EXECUTIVE REPORT — Web With Roni Private Limited\n"
        report += f"{'='*50}\n\n"
        report += f"TASK: {big_task[:200]}\n\n"
        for code, v in agent_results.items():
            report += f"[{v['agent']}] Confidence: {v['confidence']}%\n"
            report += f"{v['response'][:300]}\n\n"
        return report
