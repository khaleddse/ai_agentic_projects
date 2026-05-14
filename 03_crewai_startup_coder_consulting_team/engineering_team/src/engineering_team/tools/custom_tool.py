import subprocess
import sys
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class PythonExecutorInput(BaseModel):
    code: str = Field(..., description="Python code to execute and test")


class PythonExecutorTool(BaseTool):
    name: str = "python_executor"
    description: str = (
        "Execute Python code and return stdout and stderr. "
        "Use this to verify that code you wrote runs without errors before finalizing it."
    )
    args_schema: Type[BaseModel] = PythonExecutorInput

    def _run(self, code: str) -> str:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="output",
        )
        return (
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )


class PythonFileExecutorInput(BaseModel):
    file_path: str = Field(..., description="Path to the Python file to execute, relative to the output directory")


class PythonFileExecutorTool(BaseTool):
    name: str = "python_file_executor"
    description: str = (
        "Execute a Python file from the output directory and return its stdout/stderr. "
        "Use this to verify a generated module imports and runs correctly."
    )
    args_schema: Type[BaseModel] = PythonFileExecutorInput

    def _run(self, file_path: str) -> str:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd="output",
        )
        return (
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )


class PytestRunnerInput(BaseModel):
    test_file: str = Field(..., description="Path to the test file to run, relative to the output directory")


class PytestRunnerTool(BaseTool):
    name: str = "pytest_runner"
    description: str = (
        "Run pytest on a test file and return the results. "
        "Use this to verify that unit tests pass after writing them."
    )
    args_schema: Type[BaseModel] = PytestRunnerInput

    def _run(self, test_file: str) -> str:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd="output",
        )
        return (
            f"Return code: {result.returncode}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
