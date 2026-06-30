"""
WORKFLOW — FULL EXECUTION FLOW
CEO -> Planner -> Task Split -> Department Heads ->
Agents -> Research -> Debate -> QA -> Truth Guard ->
Executive Merge -> Final Report -> Learning Engine -> Memory
"""
from colorama import Fore, Style
from agents.base_agent import Agent, get_brain, get_web
from core.planner import TaskPlanner
from core.debate import DebateEngine
from core.qa import QAEngine
from core.truth_guard import TruthGuard
from core.thinking import ThinkingPipeline
from core.memory_router import MemoryRouter
from core.learning_engine import LearningEngine
from core.prompt_compiler import PromptCompiler
from core.agent_dna import DNA

class Workflow:
    """
    The complete Project Titan execution pipeline.
    """

    def __init__(self):
        self.brain = get_brain()
        self.web = get_web()
        self.planner = TaskPlanner(self.brain)
        self.debate_engine = DebateEngine(self.brain)
        self.qa = QAEngine(self.brain)
        self.truth_guard = TruthGuard(self.brain)

    def run_full_task(self, big_task, run_debate=True):
        """
        Full Project Titan pipeline execution.
        """
        print(f"\n{Fore.MAGENTA}{'═'*58}")
        print(f"  🚀 PROJECT TITAN — FULL WORKFLOW")
        print(f"  Task: {big_task[:50]}...")
        print(f"{'═'*58}{Style.RESET_ALL}")

        # 1. PLANNER — break into subtasks
        subtasks = self.planner.plan(big_task)

        # 2. DEBATE — if strategic decision
        debate_result = None
        if run_debate:
            debate_result = self.debate_engine.debate(big_task)

        # 3. AGENTS EXECUTE each subtask through thinking pipeline
        agent_results = {}
        for sub in subtasks:
            code = sub["agent"]
            task = sub["subtask"]

            print(f"\n{Fore.CYAN}→ {DNA[code]['name']} executing: "
                  f"{task[:40]}...{Style.RESET_ALL}")

            agent = Agent(code)
            mem = MemoryRouter(code)

            # Research evidence
            web_data = self.web.search(task[:80])
            has_evidence = bool(web_data and "No results" not in web_data)

            # Compile prompt
            compiler = PromptCompiler(DNA[code], agent.kb, self.web)
            prompt = compiler.compile(
                task, web_data=web_data, output_format="standard"
            )

            # Execute
            response = self.brain.think(prompt, mode=DNA[code].get("style","best"))

            # QA pass
            qa_result = self.qa.review(task, response)

            # Truth Guard
            verified_response, confidence = self.truth_guard.validate(
                response, has_evidence
            )

            # Learning
            learner = LearningEngine(self.brain, mem)
            learner.process(task, response, qa_result)

            agent_results[code] = {
                "agent": DNA[code]["name"],
                "task": task,
                "response": verified_response,
                "qa_passed": qa_result["passed"],
                "confidence": confidence["score"]
            }

        # 4. EXECUTIVE MERGE — final report
        final_report = self._executive_merge(
            big_task, agent_results, debate_result
        )

        return final_report

    def _executive_merge(self, big_task, agent_results, debate_result):
        combined = "\n\n".join([
            f"[{v['agent']}] (Confidence: {v['confidence']}%, "
            f"QA: {'PASS' if v['qa_passed'] else 'FLAGGED'}):\n"
            f"{v['response'][:500]}"
            for v in agent_results.values()
        ])

        debate_section = ""
        if debate_result:
            debate_section = f"""
DEPARTMENT DEBATE RESULTS:
{debate_result['decision']}
"""

        prompt = f"""You are the Chief Operating Agent compiling
the FINAL EXECUTIVE REPORT for Roni at Web With Roni Private Limited.

Original request: {big_task}

All agent outputs:
{combined}
{debate_section}

Compile into ONE final executive report using this format:

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
        return self.brain.think(prompt, mode="ensemble")
