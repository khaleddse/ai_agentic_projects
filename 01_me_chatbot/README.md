# Me Chatbot

A personal AI chatbot that impersonates Khaled Selmi on a website. Visitors can ask questions about his career, skills, and background, and the bot answers in first person using his CV and a written summary as context.

## What it does

- Loads `aboutMe/My_CV.pdf` and `aboutMe/summary.txt` at startup to build a knowledge base
- Uses `gpt-4o-mini` with a system prompt that tells the model to stay in character as Khaled
- Exposes a Gradio chat UI (runs in the browser, shareable via public link)
- Uses two OpenAI tools to send real-time Pushover notifications:
  - `record_user_details` — triggered when a visitor shares their email (potential lead)
  - `record_unknown_question` — triggered when the bot can't answer a question (knowledge gap tracking)

## Architecture

```
app.py
├── Me class
│   ├── __init__     loads CV (PDF) + summary (txt)
│   ├── system_prompt builds the persona prompt with CV context
│   ├── chat         agentic loop: calls GPT, handles tool calls, loops until done
│   └── handle_tool_call  dispatches tool_calls to Python functions
├── record_user_details   sends Pushover notification with visitor email
└── record_unknown_question  sends Pushover notification with unanswered question
```

## Setup

### 1. Environment variables

Copy the example and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Where to get it |
|---|---|
| `OPENAI_API_KEY` | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) |
| `PUSHOVER_USER` | Your user key from [pushover.net](https://pushover.net) |
| `PUSHOVER_TOKEN` | App token — create an app at pushover.net |

### 2. Add your personal data

Place your files in `aboutMe/`:

- `My_CV.pdf` — your CV in PDF format
- `summary.txt` — a short written bio / summary in plain text

### 3. Run

```bash
# from the repo root
uv run projects/01_me_chatbot/app.py

# or from inside the project folder
cd projects/01_me_chatbot
uv run app.py
```

The Gradio UI opens at `http://localhost:7860`. A shareable public link is also printed to the terminal.
