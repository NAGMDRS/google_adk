from google.adk.agents import Agent
from helperFiles.tools import search_arxiv_papers, summerizing_AgentTool

researcher_agent_1 = Agent(
    name="ResearcherAgent",
    model="gemini-2.0-flash",
    description=(
        "Agent to do research about a project from arxiv"
    ),
    instruction=(
        "You are a helpful agent who can explain the research papers *only* related to the topic "
        "and also summarize the abstracts of each paper using the summerizing_AgentTool tool"
    ),
    tools=[search_arxiv_papers, summerizing_AgentTool]
)

root_agent = researcher_agent_1