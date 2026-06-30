"""
MODULE 12 — PROMPT COMPILER
Task → Agent DNA → Memory → Evidence → Web →
Thinking Mode → Output Format → Prompt → LLM

Dynamically builds the perfect prompt instead
of one giant static template.
"""
from datetime import datetime

class PromptCompiler:
    """
    Compiles a complete, structured prompt from
    all available context sources.
    """

    def __init__(self, agent_dna, knowledge_base, web_intel=None):
        self.dna = agent_dna
        self.kb = knowledge_base
        self.web = web_intel

    def compile(self, task, context="", web_data="",
                output_format="standard", thinking_mode="standard"):
        """
        Build the complete prompt from all layers.
        """
        sections = []

        # Layer 1 — Identity
        sections.append(self._identity_block())

        # Layer 2 — Expertise
        sections.append(self._expertise_block())

        # Layer 3 — Company Context
        sections.append(self._company_block())

        # Layer 4 — Memory (Knowledge Base)
        sections.append(self._memory_block())

        # Layer 5 — Evidence / Web Data
        if web_data:
            sections.append(self._evidence_block(web_data))

        # Layer 6 — Additional Context
        if context:
            sections.append(f"ADDITIONAL CONTEXT:\n{context}")

        # Layer 7 — Task
        sections.append(self._task_block(task))

        # Layer 8 — Output Format Requirements
        sections.append(self._output_format_block(output_format))

        # Layer 9 — Thinking Mode Instructions
        sections.append(self._thinking_mode_block(thinking_mode))

        return "\n\n".join(sections)

    def _identity_block(self):
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR IDENTITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Name: {self.dna['name']}
Department: {self.dna['dept']}
Personality: {self.dna['personality']}
Core Mission: {self.dna['core']}"""

    def _expertise_block(self):
        skills = "\n".join([f"• {s}" for s in self.dna["skills"]])
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR EXPERTISE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{skills}"""

    def _company_block(self):
        from core.knowledge_base import COMPANY
        services = "\n".join([
            f"• {k}: {v}" for k,v in COMPANY["services"].items()
        ])
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPANY CONTEXT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Company: Web With Roni Private Limited
Founder: Roni (the only human — your boss)
Services:
{services}"""

    def _memory_block(self):
        ctx = self.kb.get_context()
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR MEMORY (Self-Learned)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{ctx}"""

    def _evidence_block(self, web_data):
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EVIDENCE (Real-Time Web Data)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{web_data}

RULE: Any claim using this evidence must be
marked FACT with high confidence. Any claim
NOT backed by this evidence must be marked
ASSUMPTION, ESTIMATE, or OPINION."""

    def _task_block(self, task):
        return f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TASK FROM RONI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{task}"""

    def _output_format_block(self, fmt):
        if fmt == "standard":
            return """━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure your response EXACTLY as:

EXECUTIVE SUMMARY:
[2-3 sentences]

OBJECTIVES:
[what this addresses]

ANALYSIS:
[your reasoning]

EVIDENCE:
[facts used, with source]

RISKS:
[what could go wrong]

RECOMMENDATIONS:
[specific actions]

KPIS:
[how to measure success]

ACTION PLAN:
[step by step]

CONFIDENCE:
[overall % and why]

NEXT STEP:
[immediate next action for Roni]"""
        return ""

    def _thinking_mode_block(self, mode):
        if mode == "deep":
            return """━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THINKING INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Think through this fully before answering:
1. Observe what is being asked
2. Understand the real underlying need
3. Recall relevant past learnings
4. Consider what research/evidence applies
5. Plan your approach
6. Brainstorm multiple options
7. Critically evaluate each option
8. Choose the best option
9. Execute (write the actual answer)
10. Review your own answer for errors
Show this reasoning briefly, then deliver
the final structured answer."""
        return """━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THINKING INSTRUCTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Think before answering. Be direct and accurate."""
