from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from engineering_team.tools.custom_tool import (
    PythonExecutorTool,
    PythonFileExecutorTool,
    PytestRunnerTool,
)


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],  # type: ignore[index]
            verbose=True,
            tools=[PythonFileExecutorTool(), PythonExecutorTool()],
            max_retry_limit=3,
        )

    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],  # type: ignore[index]
            verbose=True,
            tools=[PythonExecutorTool(), PythonFileExecutorTool()],
            max_retry_limit=3,
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['qa_engineer'],  # type: ignore[index]
            verbose=True,
            tools=[PytestRunnerTool(), PythonFileExecutorTool()],
            max_retry_limit=3,
        )

    @task
    def design_task(self) -> Task:
        return Task(config=self.tasks_config['design_task'])  # type: ignore[index]

    @task
    def code_task(self) -> Task:
        return Task(config=self.tasks_config['code_task'])  # type: ignore[index]

    @task
    def frontend_task(self) -> Task:
        return Task(config=self.tasks_config['frontend_task'])  # type: ignore[index]

    @task
    def qa_task(self) -> Task:
        return Task(config=self.tasks_config['qa_task'])  # type: ignore[index]

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
