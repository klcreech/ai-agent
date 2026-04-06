# 🤖 Architect AI Agents

<p align="center">
  <img src="https://cdn.simpleicons.org/python/3776AB" width="18"/> Architecting <b>Autonomous AI Agents</b> with <b>Hardware-in-the-Loop Awareness</b><br/>
  <img src="https://cdn.simpleicons.org/n8n/FF6A00" width="18"/> Engineering <b>Agentic Pipelines</b> & <b>LLM Orchestration</b> for local and cloud workflows<br/>
  <img src="https://cdn.simpleicons.org/docker/2496ED" width="18"/> Bridging <b>System-Level Discovery</b> with <b>Containerized AI Inference</b>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/kerry-creech/">
      <img src="https://img.shields.io/badge/LinkedIn-Kerry%20Creech-0A66C2?style=flat-square&logo=linkedin&logoColor=white" />
  </a>
  <a href="https://github.com/klcreech">
      <img src="https://img.shields.io/badge/GitHub-klcreech-181717?style=flat-square&logo=github&logoColor=white" />
  </a>
</p>

---

## 🧩 Overview
This project demonstrates a production-ready **AI Agent lifecycle**. Unlike standard LLM implementations, this agent is **environment-aware**, meaning it probes the host hardware and OS state before making decisions. It is designed to bridge the gap between static LLM reasoning and real-world system administration.

### Core Capabilities:
- **System Telemetry**: Deep discovery of OS, kernel, and hardware metrics.
- **Diagnostic Reasoning**: Context-aware log analysis using local LLMs.
- **Automated Remediation**: Generation of validated scripts to fix system service failures.
- **Local Inference**: Optimized for privacy and speed using Ollama.

---

## 🗂️ Project Structure

```bash
ai-agents/
└── agent-ai/
    ├── main.py          # Orchestrator: Coordinates telemetry, analysis, and remediation
    ├── agent.py         # LLM Interface: Logic for prompt engineering & Ollama interaction
    ├── system_info.py   # Telemetry: Probes CPU, RAM, and Systemd service states
    ├── analyze.txt      # Agent Output: Stores the reasoning and diagnostic history
    ├── setup.sh         # Automation: One-click environment & model setup
    └── requirements.txt # Dependencies: psutil, ollama, and core Python libs
⚙️ How it Works
Observe: system_info.py extracts real-time telemetry (e.g., "Is nginx failing? Is the CPU at 99%?").

Think: The orchestrator sends this hardware context to the LLM with a specialized "System Admin" prompt.

Plan: The agent analyzes the logs in agent.py and determines if a fix is necessary.

Act: The agent generates a precise Bash script for remediation, documented in analyze.txt.

🚀 Getting Started
1. Prerequisites
You must have Ollama installed and the qwen2.5-coder model available (the setup script can handle the model pull).

2. Installation
Bash
# Clone the repository
git clone [https://github.com/klcreech/ai-agent.git](https://github.com/klcreech/ai-agent.git)
cd ai-agent/agent-ai

# Run the automated setup (creates venv and installs deps)
bash setup.sh
3. Execution
Bash
# Activate the virtual environment
source venv/bin/activate

# Run the AI Agent
python main.py
💡 Engineering Highlights
Modular Architecture: Logic is decoupled, allowing the agent to be ported to different OS environments easily.

Safety First: Remediation scripts are presented for review, demonstrating a "Human-in-the-Loop" safety pattern for AI automation.

Local-First: No data leaves the machine. All inference is handled by the local hardware.
