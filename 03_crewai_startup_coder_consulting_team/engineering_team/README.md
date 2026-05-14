# Engineering Team — AI Code Generation Crew

A multi-agent system powered by [crewAI](https://crewai.com) that turns a plain-text requirement description into a fully working Python backend, a Gradio UI, and a passing test suite — then launches the result automatically.

## What it does

You describe what you want to build. Four AI agents collaborate in sequence to produce it:

| Agent | Role | Output |
|---|---|---|
| **Engineering Lead** | Reads your requirements and produces a detailed technical design | `output/<module>_design.md` |
| **Backend Engineer** | Implements the design as a self-contained Python module, runs it to verify there are no errors | `output/<module>.py` |
| **Frontend Engineer** | Writes a Gradio UI with a tab for every feature of the backend, validates syntax before saving | `output/app.py` |
| **QA Engineer** | Writes unit tests, runs them with pytest, and fixes failures before finishing | `output/test_<module>.py` |

After all agents finish, the generated `app.py` is launched automatically and a clickable link appears in the UI.

## Requirements

- Python 3.10 – 3.13
- [uv](https://docs.astral.sh/uv/) package manager
- An `OPENAI_API_KEY` in a `.env` file

```bash
pip install uv
```

## Setup

```bash
cd 03_crewai_startup_coder_consulting_team/engineering_team

# create .env and add your key
echo "OPENAI_API_KEY=sk-..." > .env

# install dependencies
uv sync
```

## Running

### Option 1 — Web UI (recommended)

Opens a Gradio form where you type your requirements and click **Generate & Launch**:

```bash
uv run run_ui
```

Then open [http://localhost:7860](http://localhost:7860).  
When the crew finishes a clickable link to the generated app appears automatically.

### Option 2 — CLI

Runs the hardcoded requirements in `src/engineering_team/main.py` directly:

```bash
uv run run_crew
```

Generated files are saved to the `output/` folder.

## Project structure

```
engineering_team/
├── src/engineering_team/
│   ├── config/
│   │   ├── agents.yaml   # agent roles, goals, LLM assignments
│   │   └── tasks.yaml    # task descriptions and output files
│   ├── tools/
│   │   └── custom_tool.py  # PythonExecutorTool, PythonFileExecutorTool, PytestRunnerTool
│   ├── crew.py           # wires agents, tasks, and tools together
│   ├── main.py           # CLI entry point — edit requirements here
│   └── ui.py             # Gradio input UI with auto-launch
└── output/               # all generated files land here
```

## Customising

- Change the **default requirements** in `src/engineering_team/main.py`
- Change which **LLM** each agent uses in `config/agents.yaml` (default: `gpt-4o` / `gpt-4o-mini`)
- Add new agents or tasks in `config/agents.yaml` and `config/tasks.yaml`
