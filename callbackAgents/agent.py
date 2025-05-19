from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-2.0-flash-live-001",
    name= 'Hello0o0',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge'
)