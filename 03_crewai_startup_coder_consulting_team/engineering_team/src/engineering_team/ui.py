import os
import queue
import re
import sys
import time
import threading
import subprocess
import gradio as gr

os.makedirs("output", exist_ok=True)

_output_process: subprocess.Popen | None = None


def _stop_output_app():
    global _output_process
    if _output_process and _output_process.poll() is None:
        _output_process.terminate()
        _output_process = None


def _launch_output_app() -> str:
    global _output_process
    _stop_output_app()

    try:
        _output_process = subprocess.Popen(
            [sys.executable, "-u", "app.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd="output",
            env={**os.environ, "PYTHONUNBUFFERED": "1"},
        )
    except Exception as e:
        return f"Failed to start app: {e}"

    line_queue: queue.Queue[str | None] = queue.Queue()

    def _reader():
        for line in _output_process.stdout:
            line_queue.put(line)
        line_queue.put(None)

    threading.Thread(target=_reader, daemon=True).start()

    deadline = time.time() + 30
    while time.time() < deadline:
        try:
            line = line_queue.get(timeout=1)
        except queue.Empty:
            if _output_process.poll() is not None:
                break
            continue
        if line is None:
            break
        match = re.search(r"https?://\S+", line)
        if match:
            return match.group(0).rstrip("/")

    return "http://127.0.0.1:7861"


def run_crew(requirements: str, module_name: str, class_name: str, progress=gr.Progress()):
    if not requirements.strip():
        return "Please enter requirements.", gr.update(visible=False)
    if not class_name.strip():
        return "Please enter a class name.", gr.update(visible=False)

    module_name = module_name.strip()
    if not module_name.endswith(".py"):
        module_name += ".py"

    from engineering_team.crew import EngineeringTeam

    inputs = {
        "requirements": requirements,
        "module_name": module_name,
        "module_name_no_ext": module_name.replace(".py", ""),
        "class_name": class_name.strip(),
    }

    progress(0.1, desc="Running crew — design phase...")
    try:
        EngineeringTeam().crew().kickoff(inputs=inputs)
    except Exception as e:
        return f"Crew failed:\n{e}", gr.update(visible=False)

    progress(0.9, desc="Launching generated app...")
    url = _launch_output_app()

    output_files = sorted(os.listdir("output")) if os.path.exists("output") else []
    files_list = "\n".join(f"  • {f}" for f in output_files)

    link_html = (
        f'<div style="margin-top:12px;padding:14px;background:#f0fdf4;'
        f'border:1px solid #86efac;border-radius:8px;">'
        f'<p style="margin:0 0 6px 0;font-weight:600;color:#166534;">Your app is ready!</p>'
        f'<a href="{url}" target="_blank" '
        f'style="font-size:16px;color:#1d4ed8;text-decoration:underline;">{url}</a>'
        f"</div>"
    )

    progress(1.0, desc="Done!")
    return (
        f"Crew finished!\n\nGenerated files:\n{files_list}"
    ), gr.update(value=link_html, visible=True)


def launch():
    with gr.Blocks(title="Engineering Team", theme=gr.themes.Soft()) as demo:
        gr.Markdown("# Engineering Team\nDescribe what you want to build — the crew will generate and launch it.")

        with gr.Row():
            with gr.Column(scale=2):
                requirements = gr.Textbox(
                    label="Requirements",
                    placeholder="Describe the system you want to build...",
                    lines=8,
                )
            with gr.Column(scale=1):
                module_name = gr.Textbox(label="Module name", value="my_system.py")
                class_name = gr.Textbox(label="Class name", value="MySystem")

        run_btn = gr.Button("Generate & Launch", variant="primary", size="lg")
        output_log = gr.Textbox(label="Result", lines=10, interactive=False)
        app_link = gr.HTML(visible=False)

        run_btn.click(
            fn=run_crew,
            inputs=[requirements, module_name, class_name],
            outputs=[output_log, app_link],
        )

    demo.queue()
    demo.launch()


if __name__ == "__main__":
    launch()
