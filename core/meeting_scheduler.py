"""
MEETING SCHEDULER
Agents can request/hold internal meetings with each other,
logged with agenda, discussion, and decisions — like real
internal team syncs, visible to Roni.
"""
import json, os
from datetime import datetime
from colorama import Fore, Style
from core.agent_dna import DNA

MEETING_LOG = "data/meetings.json"
os.makedirs("data", exist_ok=True)

class MeetingScheduler:
    def __init__(self, brain):
        self.brain = brain

    def hold_meeting(self, topic: str, participant_codes: list, show=True):
        from agents.base_agent import Agent
        if show:
            names = ", ".join(DNA[c]["name"] for c in participant_codes)
            print(f"\n{Fore.MAGENTA}📅 Meeting: {topic[:50]} "
                  f"— Attendees: {names}{Style.RESET_ALL}")

        transcript = [f"MEETING: {topic}"]
        agenda = f"Discuss and resolve: {topic}"

        for code in participant_codes:
            agent = Agent(code)
            statement = agent.think(
                f"You're in an internal team meeting. Agenda: {agenda}\n"
                f"So far discussed:\n{chr(10).join(transcript[-4:])}\n\n"
                f"Give your input as {DNA[code]['name']} — 2-3 sentences, direct.",
                use_web=False
            )
            transcript.append(f"[{DNA[code]['name']}]: {statement}")
            if show:
                print(f"{Fore.CYAN}  🗣️ {DNA[code]['name']}: "
                      f"{statement[:90]}{Style.RESET_ALL}")

        # Meeting owner (first participant) summarizes decision
        owner_code = participant_codes[0]
        from agents.base_agent import Agent as A
        owner = A(owner_code)
        decision = owner.think(
            f"As meeting chair, summarize the DECISION reached "
            f"in 2-3 sentences from this discussion:\n"
            + "\n".join(transcript), use_web=False
        )

        record = {
            "topic": topic,
            "date": datetime.now().isoformat(),
            "attendees": [DNA[c]["name"] for c in participant_codes],
            "transcript": transcript,
            "decision": decision
        }
        self._save(record)
        return record

    def _save(self, record):
        try:
            with open(MEETING_LOG) as f:
                meetings = json.load(f)
        except:
            meetings = []
        meetings.append(record)
        with open(MEETING_LOG, "w") as f:
            json.dump(meetings, f, indent=2)

    def list_meetings(self, limit=10):
        try:
            with open(MEETING_LOG) as f:
                meetings = json.load(f)
            return meetings[-limit:]
        except:
            return []
