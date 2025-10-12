# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from tools.rag_tools import rag_tool
from typing import List
import os
from dotenv import load_dotenv
load_dotenv()


model = "openai/gpt-4o-mini"
manager_model = "openai/o3"

llm = LLM(model=model, api_key=os.environ['OPENAI_API_KEY'])
manager_llm = LLM(model=manager_model, api_key=os.environ['OPENAI_API_KEY'])


@CrewBase
class LatestAiDevelopmentCrew():
    """LatestAiDevelopment crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def auditor(self) -> Agent:
        return Agent(
            config=self.agents_config['auditor'],  # type: ignore[index]
            verbose=True,
            llm=llm
        )

    @task
    def auditor_task(self) -> Task:
        return Task(
            config=self.tasks_config['auditor_task'],  # type: ignore[index]
            tools=[rag_tool]
        )

    @task
    def analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyst_task'],
        )

    manager = Agent(
        role="Project Manager",
        goal="Efficiently manage the crew and ensure high-quality task completion",
        backstory="You're an experienced project manager, skilled in overseeing complex projects and guiding teams to success."
        "You must make sure that you have completely finished all your tasks before generating final output. Do not output an incomplete answer.",
        allow_delegation=True,
        llm=manager_llm
    )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.hierarchical,
            manager_agent=self.manager,
            verbose=True,
        )
