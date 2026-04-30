# AI Agents

A collection of small, self-contained AI agent projects. Each project lives in its own folder and can be run independently. All share a single Python virtual environment managed by [uv](https://docs.astral.sh/uv/).

## Projects

| Folder | What it does |
|---|---|
| `01_me_chatbot/` | Gradio chatbot that impersonates you — answers questions about your career using your CV and a summary file |
| `02_deep_research/` | Multi-agent research tool: plans searches, scrapes the web, writes a detailed report, and emails it via SendGrid |

---

## Quick start

### 1. Clone and set up the environment

```bash
git clone <repo-url>
cd ai_agents

# create the virtual environment and install all dependencies
uv venv
uv pip install -e .
```

### 2. Set your environment variables

Create a `.env` file at the root:

```bash
cp 01_me_chatbot/.env.example .env   # then fill in your keys
```

---

## Running each project

### Me Chatbot (`01_me_chatbot/`)

A Gradio chat UI that answers questions about your background, using your CV (PDF) and a personal summary as context. When a visitor shares their email the bot records it via Pushover.

**Required env vars:**
```
OPENAI_API_KEY=...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

**Required files** (not in git — add your own):
```
01_me_chatbot/aboutMe/My_CV.pdf
01_me_chatbot/aboutMe/summary.txt
```

**Run:**
```bash
cd 01_me_chatbot
uv run app.py
```
Opens at `http://localhost:7860`.

---

### Deep Research (`deep_research/`)

Type a research question → 4 agents kick off in parallel:

1. **Planner** — breaks the question into 5 targeted web searches
2. **Search agents** — run all searches concurrently and summarise each result
3. **Writer** — synthesises findings into a 1000+ word markdown report
4. **Email agent** — formats the report as HTML and sends it via SendGrid

**Required env vars:**
```
OPENAI_API_KEY=...
SENDGRID_API_KEY=...
```

Before running, update the sender/recipient emails in `deep_research/email_agent.py`:
```python
from_email = Email("you@yourdomain.com")   # must be a verified SendGrid sender
to_email   = To("recipient@example.com")
```

**Run:**
```bash
cd deep_research
uv run deep_research.py
```
Opens a Gradio UI in your browser. Enter a topic and click **Run**.

---

## Project structure

```
ai_agents/
├── .env                   # your local secrets (never committed)
├── pyproject.toml         # shared dependencies for all projects
├── .venv/                 # shared virtual environment
├── 01_me_chatbot/
│   ├── app.py
│   ├── aboutMe/           # your CV and summary (never committed)
│   └── README.md
└── deep_research/
    ├── deep_research.py   # entry point (Gradio UI)
    ├── research_manager.py
    ├── planner_agent.py
    ├── search_agent.py
    ├── writer_agent.py
    └── email_agent.py
```
