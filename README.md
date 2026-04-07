# Autonomous AI Agent — Hardware-in-the-Loop

Architecting autonomous AI agents with real system awareness. This isn't a chatbot wrapper — it's an agent that probes its environment, reasons over what it finds, and takes action. Built for local and cloud workflows, it bridges the gap between LLM reasoning and actual system state.

<div align="center">

![Autonomous AI Agents](https://img.shields.io/badge/Autonomous-AI_Agents-00E5FF?style=flat-square)
![Agent Lifecycle Design](https://img.shields.io/badge/Agent-Lifecycle_Design-00FFFF?style=flat-square)
![LLM Orchestration](https://img.shields.io/badge/LLM-Orchestration-00BFFF?style=flat-square)
![Context & System Awareness](https://img.shields.io/badge/Context-System_Awareness-00E5FF?style=flat-square)
![Local-First AI Systems](https://img.shields.io/badge/Local_First-AI_Systems-00FFFF?style=flat-square)
![Safe Automation](https://img.shields.io/badge/Execution-Safe_Automation-00BFFF?style=flat-square)

</div>

---

## ⚙️ What it does

Most LLM implementations are stateless — they know nothing about the machine they're running on. This agent is different. Before it does anything, it reads the environment: OS state, kernel info, hardware metrics, running services. That context becomes the foundation for everything it decides next.

From there it can diagnose failing services, analyze logs, generate remediation scripts, and document its own reasoning — all without leaving the machine. Everything runs locally through Ollama, so no data goes anywhere it shouldn't.

- **System Telemetry** — deep discovery of OS, kernel, and hardware metrics
- **Diagnostic Reasoning** — context-aware log analysis using local LLMs
- **Automated Remediation** — generates validated Bash scripts to fix service failures
- **Local Inference** — privacy-first, optimized for speed with Ollama

---

## ⚙️ Project structure
```text
ai-agents/
├── main.py          # Orchestrator — coordinates telemetry, analysis, and remediation
├── agent.py         # LLM interface — prompt engineering and Ollama interaction
├── system_info.py   # Telemetry — probes CPU, RAM, and systemd service states
├── analyze.txt      # Agent output — reasoning and diagnostic history
├── setup.sh         # One-click environment and model setup
└── requirements.txt # Dependencies
```

---

## ⚙️ How it works

**Observe** — `system_info.py` pulls real-time telemetry. Is nginx failing? Is CPU pegged at 99%? It knows before anything else runs.

**Think** — The orchestrator packages that hardware context into a specialized system admin prompt and hands it to the LLM.

**Plan** — `agent.py` analyzes the data and determines whether intervention is needed and what form it should take.

**Act** — The agent produces a precise Bash remediation script, logged to `analyze.txt` for review before anything executes.

---

## ⚙️ Getting started

Prerequisites: Ollama installed with the `qwen2.5-coder` model available. The setup script can handle the model pull if needed.
```bash
# Clone the repository
git clone https://github.com/klcreech/ai-agent.git
cd ai-agents

# Run automated setup (creates venv and installs dependencies)
bash setup.sh

# Activate and run
source venv/bin/activate
python main.py
```

---

## ⚙️ Engineering notes

**Modular by design** — telemetry, reasoning, and execution are fully decoupled. Porting to a different OS environment means swapping one module, not rewriting the whole thing.

**Human-in-the-loop safety** — remediation scripts are surfaced for review before execution. The agent can recommend, but a human confirms. That's intentional.

**Local-first** — all inference runs on-device. Nothing leaves the machine.
