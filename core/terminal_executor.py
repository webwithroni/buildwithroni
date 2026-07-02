"""
SANDBOXED TERMINAL EXECUTOR
Whitelist-only command execution. No arbitrary shell.
Every command is checked against an explicit allowlist.
Anything destructive or unlisted is REFUSED, not attempted.
"""
import subprocess, shlex
from colorama import Fore, Style

# Only these exact command prefixes are ever allowed
WHITELIST = [
    "git status", "git log", "git diff", "git branch",
    "ls", "pwd", "cat ", "head ", "tail ", "wc ",
    "python --version", "pip list", "python -m pytest",
    "find . -name", "grep -r", "df -h", "du -sh",
    "echo ", "date", "whoami"
]

BLOCKED_ALWAYS = [
    "rm ", "rm -rf", "sudo", "su ", "chmod 777", "curl ", "wget ",
    ">/dev", "dd if=", "mkfs", "kill ", "pkill", ":(){ :|:& };:",
    "eval ", "exec(", "> /", "mv /", "format ", "del /", "shutdown",
    "reboot", "passwd", "ssh ", "scp "
]

class TerminalExecutor:

    def __init__(self, timeout=15):
        self.timeout = timeout
        self.log = []

    def is_safe(self, command: str) -> tuple:
        cmd = command.strip()
        cmd_lower = cmd.lower()

        for blocked in BLOCKED_ALWAYS:
            if blocked in cmd_lower:
                return False, f"Blocked: contains forbidden pattern '{blocked}'"

        for allowed_prefix in WHITELIST:
            if cmd_lower.startswith(allowed_prefix.lower()):
                return True, "Whitelisted"

        return False, "Not in whitelist — requires manual approval"

    def execute(self, command: str, approved_by_roni=False):
        safe, reason = self.is_safe(command)

        if not safe and not approved_by_roni:
            result = {
                "command": command,
                "executed": False,
                "output": f"❌ Refused: {reason}. "
                          f"Set approved_by_roni=True to override for this one command.",
                "safe": False
            }
            self.log.append(result)
            return result

        try:
            proc = subprocess.run(
                shlex.split(command),
                capture_output=True, text=True,
                timeout=self.timeout
            )
            output = proc.stdout if proc.returncode == 0 else proc.stderr
            result = {
                "command": command,
                "executed": True,
                "output": output[:3000],
                "returncode": proc.returncode,
                "safe": safe
            }
        except subprocess.TimeoutExpired:
            result = {"command": command, "executed": False,
                       "output": "⏱️ Timed out", "safe": safe}
        except Exception as e:
            result = {"command": command, "executed": False,
                       "output": f"Error: {e}", "safe": safe}

        self.log.append(result)
        return result
