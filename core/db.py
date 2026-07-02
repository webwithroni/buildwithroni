import sqlite3, os, json
from datetime import datetime

DB_PATH = "data/webwithroni.db"
os.makedirs("data", exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT, business TEXT, contact TEXT,
        status TEXT DEFAULT 'lead', notes TEXT,
        created TEXT
    );
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prompt TEXT, agent TEXT, response TEXT,
        complexity TEXT, created TEXT
    );
    """)
    conn.commit()
    conn.close()

def add_client(name, business, contact, status="lead", notes=""):
    conn = get_conn()
    conn.execute(
        "INSERT INTO clients (name,business,contact,status,notes,created) VALUES (?,?,?,?,?,?)",
        (name, business, contact, status, notes, datetime.now().isoformat())
    )
    conn.commit(); conn.close()

def list_clients():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM clients ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_task(prompt, agent, response, complexity):
    conn = get_conn()
    conn.execute(
        "INSERT INTO tasks (prompt,agent,response,complexity,created) VALUES (?,?,?,?,?)",
        (prompt, agent, response, complexity, datetime.now().isoformat())
    )
    conn.commit(); conn.close()

def list_tasks(limit=20):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
