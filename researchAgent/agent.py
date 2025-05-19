from google.adk.agents import Agent
from google.adk.memory.base_memory_service import MemoryResult

from helperFiles.tools import search_arxiv_papers, summerising_AgentTool
from google.adk.tools import load_memory, ToolContext
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
import inspect

APP_NAME = "researchAgent_app"
USER_ID = "nagmdrs_1"
SESSION_ID = "session_001"

session_service = InMemorySessionService()
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

root_agent = Agent(
    name="ResearcherAgent",
    model="gemini-2.0-flash-live-001",
    description=(
        "Agent to do research about a project from arxiv"
    ),
    instruction=(
        """You are a specialized assistant that explains research papers strictly related to the given topic. For 
        each paper, you must also summarize the abstract using the summarizing_AgentTool.Before processing a new 
        request, check the memory for any previously asked similar questions. If a matching question is found, 
        return the original response from memory and clearly inform the user that the answer has been retrieved from 
        memory to avoid duplication"""
    ),
    tools=[search_arxiv_papers, summerising_AgentTool, load_memory]
)

memory_service = InMemoryMemoryService()
runner = Runner(
    app_name="my_app",
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service
)


def load_memory(query: str, tool_context: ToolContext) -> 'list[MemoryResult]':
    """Loads the memory for the current user."""
    response = tool_context.search_memory(query)
    return response.coroutines


async def safe_add_session_to_memory(memory_service, session):
    """Handle either sync or async add_session_to_memory method."""
    result = memory_service.add_session_to_memory(session)
    if inspect.iscoroutine(result):
        return await result
    return result


async def handle_conversation_async(query_text):
    """Handle a conversation asynchronously."""
    user_message = types.Content(
        parts=[types.Part(text=query_text)]
    )

    response = ""
    async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=user_message
    ):
        if event.author == root_agent.name and event.content:
            parts = event.content.parts
            for part in parts:
                if hasattr(part, 'text') and part.text:
                    response += part.text

    return response


def handle_conversation(query_text):
    """Synchronous wrapper for the async conversation handler."""
    return asyncio.run(handle_conversation_async(query_text))


if __name__ == "__main__":
    user_query = input("Enter your research topic: ")

    response = handle_conversation(user_query)
    print(response)

    session = session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    runner.close_session(session)
