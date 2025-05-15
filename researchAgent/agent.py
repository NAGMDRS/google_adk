from google.adk.agents import Agent
from helperFiles.tools import search_arxiv_papers, summerizing_AgentTool
from google.adk.tools import load_memory
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types


root_agent = Agent(
    name="ResearcherAgent",
    model="gemini-2.0-flash",
    description=(
        "Agent to do research about a project from arxiv"
    ),
    instruction=(
        """You are a helpful agent who can explain the research papers *only* related to the topic and also summarize 
        the abstracts of each paper using the summerizing_AgentTool tool also check in memory 
        if same question was asked previously and also save to memory after every query"""
    ),
    tools=[search_arxiv_papers, summerizing_AgentTool,load_memory]
)

session_service = InMemorySessionService()
memory_service = InMemoryMemoryService()

runner = Runner(
    app_name="my_app",
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service
)
