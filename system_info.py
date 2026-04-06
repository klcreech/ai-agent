import subprocess
import os
import platform

def get_system_context():
    distro = platform.linux_distribution()[0] if hasattr(platform, 'linux_distribution') else platform.system()
    
    context = {
        "os": platform.system(),
        "distro": distro,
        "kernel": platform.release(),
        "pkg_manager": "pacman" if os.path.exists("/usr/bin/pacman") else "apt" if os.path.exists("/usr/bin/apt") else "brew",
        "env_type": "Container" if os.path.exists("/.dockerenv") else "Host System"
    }

    # Universal Log Retrieval
    try:
        if context["os"] == "Linux":
            # Get last 20 lines of critical/error logs from journald
            cmd = ["journalctl", "-p", "3", "-n", "20", "--no-pager"]
            context["recent_logs"] = subprocess.check_output(cmd).decode('utf-8')
        elif context["os"] == "Darwin": # macOS
            context["recent_logs"] = subprocess.check_output(["log", "show", "--predicate", "eventMessage contains 'error'", "--last", "10m"]).decode('utf-8')
    except Exception:
        context["recent_logs"] = "No critical errors detected or logger unavailable."

    return context