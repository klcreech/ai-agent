import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm

from system_info import get_system_context
from agent import call_llm

console = Console()


def main():
    console.print(Panel.fit("[bold]ARCHITECT AI AGENT[/bold]", border_style="white"))

    # 🔍 Phase 1: System Info
    with console.status("[bold]Gathering system telemetry...[/bold]"):
        ctx = get_system_context()

    console.print(f"OS: {ctx['distro']} | Kernel: {ctx['kernel']}")

    logs = ctx.get("recent_logs", "")

    # 🚫 Exit early if nothing useful
    if not logs.strip() or "No critical errors" in logs:
        console.print("[bold green]System status: Nominal.[/bold green]")
        return

    # 🧠 Phase 2: Diagnostic
    ctx["mode"] = "diagnostic"
    with console.status("[bold]Analyzing logs...[/bold]"):
        report = call_llm(ctx, logs)

    if report:
        console.print(
            Panel(
                Markdown(report),
                title="[bold]DIAGNOSTIC[/bold]",
                border_style="white"
            )
        )
    else:
        console.print("[yellow]No diagnostic output.[/yellow]")

    # 🔧 Phase 3: Remediation
    if not Confirm.ask("\nGenerate remediation script?"):
        return

    ctx["mode"] = "remediation"
    with console.status("[bold]Generating fix script...[/bold]"):
        script = call_llm(ctx, logs)

    # ✅ Handle "no fix needed"
    if not script:
        console.print("[bold green][✓] No systemd failures detected. No fix needed.[/bold green]")
        return

    # 💾 Save script if it contains real fixes
    with open("fix_system.sh", "w") as f:
        f.write(script)

    os.chmod("fix_system.sh", 0o755)
    console.print("[bold cyan][+] fix_system.sh created[/bold cyan]")

    # 👀 Show preview before execution
    console.print(
        Panel(
            script,
            title="[bold]SCRIPT PREVIEW[/bold]",
            border_style="yellow"
        )
    )

    # ⚠️ Final confirmation
    if not Confirm.ask("Execute this script with sudo?"):
        console.print("[yellow]Execution cancelled[/yellow]")
        return

    console.print("[bold red]Running script...[/bold red]")
    os.system("sudo ./fix_system.sh")

    console.print("[green]Fix applied. Monitoring...[/green]")
    time.sleep(3)
    console.print("[bold]Done.[/bold]")


if __name__ == "__main__":
    main()