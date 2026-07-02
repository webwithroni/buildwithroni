#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
load_dotenv()

from agents.base_agent import Agent, get_brain, get_web
from core.auto_router import AutoRouter
from core.workflow import Workflow
from core.agent_dna import DNA, DEPARTMENTS
from core.rate_guard import RateGuard
from core.personality import personality_block
from core import db

db.init_db()

app = Flask(__name__, static_folder="web", static_url_path="")

brain = get_brain()
web = get_web()
router = AutoRouter(brain)
guard = RateGuard(brain)
workflow = Workflow()

# Simple in-memory conversation history (single-user, resets on restart)
SESSION_HISTORY = []
MAX_HISTORY = 10

def history_block():
    if not SESSION_HISTORY:
        return ""
    lines = "\n".join([
        f"Roni: {h['prompt']}\nYou: {h['response'][:150]}"
        for h in SESSION_HISTORY[-MAX_HISTORY:]
    ])
    return f"\nRecent conversation:\n{lines}\n"

@app.route("/")
def index():
    return send_from_directory("web", "index.html")

@app.route("/api/team")
def team():
    out = []
    for dept, keys in DEPARTMENTS.items():
        for k in keys:
            out.append({"code": k, "dept": dept, **DNA[k]})
    return jsonify(out)

@app.route("/api/status")
def status():
    return jsonify({
        "models_online": brain.online_count,
        "search_online": len(web.available),
        "agents": sum(len(v) for v in DEPARTMENTS.values()),
        "calls": guard.status()
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "").strip()
    deep = data.get("deep", False)
    if not prompt:
        return jsonify({"error": "empty prompt"}), 400

    decision = router.classify(prompt)
    hist = history_block()

    if decision["complexity"] == "CASUAL":
        # Lightweight, human, no corporate formatting
        casual_prompt = f"""You are the Chief Operating Agent (COA) at
Web With Roni Private Limited — but right now you're just
talking casually with Roni, the founder, like a real colleague.

{hist}
Roni just said: "{prompt}"

Reply naturally and briefly (1-3 sentences max).
NO headers, NO bullet points, NO tables, NO reports.
Just talk like a real person would."""
        result = guard.think(casual_prompt, mode="fast")
        agent_used = "Chief Operating Agent (COA)"

    elif decision["complexity"] == "COMPLEX":
        result = workflow.run_full_task(prompt)
        agent_used = "Full Workflow"

    else:
        code = decision["agent"]
        agent = Agent(code)
        agent_used = f"{DNA[code]['name']} ({code})"
        enriched = f"{hist}\nCurrent request: {prompt}" if hist else prompt
        if deep:
            ctx = personality_block(code, situation=prompt)
            result = guard.think(f"{ctx}\n\nTask: {enriched}", mode=DNA[code].get("style","best"))
        else:
            result = agent.think(enriched)

    SESSION_HISTORY.append({"prompt": prompt, "response": result})
    if len(SESSION_HISTORY) > 30:
        SESSION_HISTORY.pop(0)

    db.save_task(prompt, agent_used, result, decision["complexity"])
    return jsonify({
        "agent": agent_used,
        "response": result,
        "complexity": decision["complexity"]
    })

@app.route("/api/clients", methods=["GET", "POST"])
def clients():
    if request.method == "POST":
        d = request.json
        db.add_client(d.get("name",""), d.get("business",""),
                       d.get("contact",""), d.get("status","lead"),
                       d.get("notes",""))
        return jsonify({"ok": True})
    return jsonify(db.list_clients())

@app.route("/api/tasks")
def tasks():
    return jsonify(db.list_tasks())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

# ══════════════════════════════════════
# ENTERPRISE UPGRADE ENDPOINTS
# ══════════════════════════════════════
from core.terminal_executor import TerminalExecutor
from core.meeting_scheduler import MeetingScheduler
from core.evolution_engine import EvolutionEngine
from core.experience import Experience

terminal = TerminalExecutor()
meetings = MeetingScheduler(brain)
evolution = EvolutionEngine(brain)

@app.route("/api/terminal", methods=["POST"])
def run_terminal():
    cmd = request.json.get("command", "")
    approved = request.json.get("approved", False)
    result = terminal.execute(cmd, approved_by_roni=approved)
    return jsonify(result)

@app.route("/api/meeting", methods=["POST"])
def hold_meeting():
    d = request.json
    topic = d.get("topic", "")
    participants = d.get("participants", ["COA", "CTO"])
    record = meetings.hold_meeting(topic, participants, show=False)
    return jsonify(record)

@app.route("/api/meetings")
def list_meetings():
    return jsonify(meetings.list_meetings())

@app.route("/api/experience/<code>")
def agent_experience(code):
    exp = Experience(code)
    return jsonify(exp.status())
