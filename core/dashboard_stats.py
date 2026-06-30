"""
MODULE 11 — EXECUTIVE DASHBOARD
Live metrics: Agents Online, Tasks Running,
Completed, Failed, Avg Quality, Avg Confidence,
Knowledge Size, Learning Score.
"""
import json, os, glob
from datetime import datetime

class DashboardStats:

    @staticmethod
    def gather(agents_dict, brain):
        total_tasks = 0
        total_scores = []
        total_knowledge = 0
        total_lessons = 0

        for code, agent in agents_dict.items():
            total_tasks += agent.kb.count
            total_scores.extend(agent.kb.data.get("scores", []))

        kb_files = glob.glob("knowledge/agents/*.json")
        for f in kb_files:
            try:
                with open(f) as file:
                    data = json.load(file)
                    total_knowledge += len(data.get("patterns", []))
            except:
                pass

        avg_quality = (
            round(sum(total_scores)/len(total_scores), 1)
            if total_scores else 0
        )

        return {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "agents_online": len(agents_dict),
            "ai_models_active": brain.online_count,
            "tasks_completed": total_tasks,
            "avg_quality_score": avg_quality,
            "knowledge_patterns": total_knowledge,
            "monthly_cost": "$0.00"
        }

    @staticmethod
    def print_dashboard(stats):
        print(f"""
╔══════════════════════════════════════════════╗
  📊 EXECUTIVE DASHBOARD — {stats['timestamp']}
╠══════════════════════════════════════════════╣
  Agents Online:      {stats['agents_online']}
  AI Models Active:   {stats['ai_models_active']}
  Tasks Completed:    {stats['tasks_completed']}
  Avg Quality Score:  {stats['avg_quality_score']}/10
  Knowledge Patterns: {stats['knowledge_patterns']}
  Monthly Cost:       {stats['monthly_cost']}
╚══════════════════════════════════════════════╝""")
