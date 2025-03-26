# src/dev_team_crew/crew.py
import os
from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, DirectoryReadTool, FileReadTool
#from langchain_anthropic import ChatAnthropic  # Import Anthropic's chat model

@CrewBase
class DevTeamCrew:
    """Development Team Crew for software projects"""
    
    agents_config = "config/agents.yaml"  # Path to YAML config files
    tasks_config = "config/tasks.yaml"

     # Create the LLM instance using Anthropic's Claude
    anthropic_llm = LLM(
        model="anthropic/claude-3-haiku-20240307",  # Note the 'anthropic/' prefix
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
        temperature=0.7
    )
    
    @agent
    def tech_lead(self) -> Agent:
        """Technical Lead agent responsible for architecture and planning"""
        return Agent(
            role=self.agents_config["tech_lead"]["role"],
            goal=self.agents_config["tech_lead"]["goal"],
            backstory=self.agents_config["tech_lead"]["backstory"],
            verbose=True,
            tools=[SerperDevTool(), DirectoryReadTool(), FileReadTool()],
            llm=self.anthropic_llm  # Use Anthropic's Claude
        )
    
    @agent
    def frontend_dev(self) -> Agent:
        """Frontend Developer agent responsible for UI implementation"""
        return Agent(
            role=self.agents_config["frontend_dev"]["role"],
            goal=self.agents_config["frontend_dev"]["goal"],
            backstory=self.agents_config["frontend_dev"]["backstory"],
            verbose=True,
            tools=[SerperDevTool(), FileReadTool()],
            llm=self.anthropic_llm  # Use Anthropic's Claude
        )
    
    @agent
    def backend_dev(self) -> Agent:
        """Backend Developer agent responsible for server-side implementation"""
        return Agent(
            role=self.agents_config["backend_dev"]["role"],
            goal=self.agents_config["backend_dev"]["goal"],
            backstory=self.agents_config["backend_dev"]["backstory"],
            verbose=True,
            tools=[SerperDevTool(), FileReadTool()],
            llm=self.anthropic_llm  # Use Anthropic's Claude
        )
    
    @agent
    def qa_engineer(self) -> Agent:
        """QA Engineer agent responsible for testing strategies"""
        return Agent(
            role=self.agents_config["qa_engineer"]["role"],
            goal=self.agents_config["qa_engineer"]["goal"],
            backstory=self.agents_config["qa_engineer"]["backstory"],
            verbose=True,
            tools=[FileReadTool()],
            llm=self.anthropic_llm  # Use Anthropic's Claude
        )
    
    @agent
    def devops_engineer(self) -> Agent:
        """DevOps Engineer agent responsible for deployment strategies"""
        return Agent(
            role=self.agents_config["devops_engineer"]["role"],
            goal=self.agents_config["devops_engineer"]["goal"],
            backstory=self.agents_config["devops_engineer"]["backstory"],
            verbose=True,
            tools=[SerperDevTool(), FileReadTool()],
            llm=self.anthropic_llm  # Use Anthropic's Claude
        )
    
    @task
    def architecture_design(self) -> Task:
        """Architecture design task"""
        return Task(
            description=self.tasks_config["architecture_design"]["description"],
            agent=self.tech_lead(),
            expected_output=self.tasks_config["architecture_design"]["expected_output"],
            output_file=self.tasks_config["architecture_design"]["output_file"]
        )
    
    @task
    def frontend_implementation(self) -> Task:
        """Frontend implementation planning task"""
        return Task(
            description=self.tasks_config["frontend_implementation"]["description"],
            agent=self.frontend_dev(),
            expected_output=self.tasks_config["frontend_implementation"]["expected_output"],
            context=[self.architecture_design()],
            output_file=self.tasks_config["frontend_implementation"]["output_file"]
        )
    
    @task
    def backend_implementation(self) -> Task:
        """Backend implementation planning task"""
        return Task(
            description=self.tasks_config["backend_implementation"]["description"],
            agent=self.backend_dev(),
            expected_output=self.tasks_config["backend_implementation"]["expected_output"],
            context=[self.architecture_design()],
            output_file=self.tasks_config["backend_implementation"]["output_file"]
        )
    
    @task
    def test_plan(self) -> Task:
        """Test planning task"""
        return Task(
            description=self.tasks_config["test_plan"]["description"],
            agent=self.qa_engineer(),
            expected_output=self.tasks_config["test_plan"]["expected_output"],
            context=[self.architecture_design(), self.frontend_implementation(), self.backend_implementation()],
            output_file=self.tasks_config["test_plan"]["output_file"]
        )
    
    @task
    def deployment_plan(self) -> Task:
        """Deployment strategy planning task"""
        return Task(
            description=self.tasks_config["deployment_plan"]["description"],
            agent=self.devops_engineer(),
            expected_output=self.tasks_config["deployment_plan"]["expected_output"],
            context=[self.architecture_design(), self.frontend_implementation(), self.backend_implementation(), self.test_plan()],
            output_file=self.tasks_config["deployment_plan"]["output_file"]
        )
    
    @crew
    def crew(self) -> Crew:
        """Assemble the development team crew"""
        return Crew(
            agents=[
                self.tech_lead(),
                self.frontend_dev(),
                self.backend_dev(),
                self.qa_engineer(),
                self.devops_engineer()
            ],
            tasks=[
                self.architecture_design(),
                self.frontend_implementation(),
                self.backend_implementation(),
                self.test_plan(),
                self.deployment_plan()
            ],
            process=Process.sequential,
            verbose=True
        )