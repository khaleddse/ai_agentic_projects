# AI Agents

A collection of small, self-contained AI agentic projects.

## Structure

```
ai_agents/
├── projects/
│   ├── 01_hello_agent/     # starter example
│   ├── 02_web_researcher/  # ...
│   └── ...
└── README.md
```

Each project under `projects/` is independent — its own dependencies, entry point, and README.

## Setup

Uses [uv](https://docs.astral.sh/uv/) workspaces. To work on a specific project:

```bash
cd projects/<project-name>
uv run main.py
```
