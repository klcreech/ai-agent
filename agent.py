import requests
import os
import re
import subprocess

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")


def get_failed_services():
    """
    Returns a list of systemd service names that are currently failed.
    """
    try:
        result = subprocess.run(
            ["systemctl", "--failed", "--no-legend", "--plain"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().splitlines()
        failed_services = []
        for line in lines:
            parts = line.split()
            if parts:
                failed_services.append(parts[0])
        return failed_services
    except Exception:
        return []


def call_llm(context, logs):
    is_remediation = context.get("mode") == "remediation"

    if is_remediation:
        failed_services = get_failed_services()
        context["failed_services"] = failed_services

        # If no failed services, return None immediately
        if not failed_services:
            return None

        system_msg = (
            "You are an Arch Linux SRE.\n"
            "Generate a SAFE bash script based ONLY on REAL errors.\n\n"
            "RULES:\n"
            "- ONLY act on real systemd/service failures\n"
            "- NEVER modify /sys, /proc, firmware, kernel\n"
            "- Output ONLY raw bash (no explanation)\n"
        )
    else:
        system_msg = (
            f"You are a Senior SRE for {context.get('distro', 'Linux')}.\n"
            "Analyze logs and output:\n\n"
            "Error:\nCause:\nFix:\n\n"
            "IGNORE ACPI, BIOS, and kernel warnings.\n"
        )

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_msg}\n\nContext:\n{context}\n\nLogs:\n{logs}",
        "stream": False,
        "options": {
            "temperature": 0.0 if is_remediation else 0.4,
            "top_p": 0.9
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=90)
        response.raise_for_status()

        content = response.json().get("response", "").strip()

        if not content:
            return None

        if is_remediation:
            # --- Extract from markdown if present ---
            if "```" in content:
                match = re.search(r"```(?:bash|sh)?\n(.*?)```", content, re.DOTALL)
                if match:
                    content = match.group(1).strip()

            # --- Remove non-code lines until a command starts ---
            lines = content.splitlines()
            cleaned = []
            code_started = False
            for line in lines:
                if not code_started and any(cmd in line for cmd in ["systemctl", "pacman"]):
                    code_started = True
                if code_started:
                    cleaned.append(line)
            content = "\n".join(cleaned).strip()

            # --- Remove dangerous commands ---
            dangerous_patterns = ["/sys", "/proc", "acpi", "dsdt", "mkfs", "dd ", "rm -rf /"]
            safe_lines = [l for l in content.splitlines() if not any(p in l.lower() for p in dangerous_patterns)]
            content = "\n".join(safe_lines).strip()

            # --- Validate services ---
            valid_services = ["bluetooth", "NetworkManager", "greetd", "dbus", "systemd-logind"]
            filtered_lines = []
            for line in content.splitlines():
                if "systemctl" in line:
                    if not any(svc in line for svc in valid_services):
                        continue
                filtered_lines.append(line)
            content = "\n".join(filtered_lines).strip()

            if not content:
                return None

        return content

    except Exception as e:
        return f"Error: {str(e)}"