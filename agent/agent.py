from google.adk.agents import Agent, LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import google_search

prompt_writer_agent = LlmAgent(
    name="PromptWriter",
    model="gemini-2.0-flash",
    instruction="""You are a professional Prompt engineer, Based on the project of user's interest, write a prompt to 
    an llm which will generate a code. You need to keep your prompt clean and precise highlighting the requirements 
    of the project. And ask the subsequent model to generate the code for the requested project. Keep prompt compact""",
    description="Writes a prompt to an llm which will generate a code for the requested project",
    output_key="generated_prompt"
)

code_writer_agent = LlmAgent(
    name="CodeWriterAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Python Code Generator.
Based *only* on the user's request, write Python code that fulfills the requirement.
Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```). 
Do not add any other text before or after the code block.

User Prompt: {generated_prompt}
""",
    description="Writes initial Python code based on a specification.",
    output_key="generated_code"
)

# Code Reviewer Agent
code_reviewer_agent = LlmAgent(
    name="CodeReviewerAgent",
    model="gemini-2.0-flash",
    instruction="""You are an expert Python Code Reviewer. 
    Your task is to provide constructive feedback on the provided code.

    **Code to Review:**
    ```python
    {generated_code}
    ```

**Review Criteria:**
1.  **Correctness:** Does the code work as intended? Are there logic errors?
2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
5.  **Best Practices:** Does the code follow common Python best practices?

**Output:**
Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
If the code is excellent and requires no changes, simply state: "No major issues found."
Output *only* the review comments or the "No major issues" statement.
""",
    description="Reviews code and provides feedback.",
    output_key="review_comments",
)

# Code Refactorer Agent
code_refactorer_agent = LlmAgent(
    name="CodeRefactorerAgent",
    model="gemini-2.0-flash",
    instruction="""You are a Python Code Refactoring AI.
Your goal is to improve the given Python code based on the provided review comments.

  **Original Code:**
  ```python
  {generated_code}
  ```

  **Review Comments:**
  {review_comments}

**Task:**
Carefully apply the suggestions from the review comments to refactor the original code.
If the review comments state "No major issues found," return the original code unchanged.
Ensure the final code is complete, functional, and includes necessary imports and docstrings.

**Output:**
Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```). 
Do not add any other text before or after the code block.
""",
    description="Refactors code based on review comments.",
    output_key="refactored_code",
)

sequential_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[prompt_writer_agent, code_writer_agent, code_reviewer_agent, code_refactorer_agent],
    description="Executes a sequence of code writing, reviewing, and refactoring.",
    # Prompt Generator -> Writer -> Reviewer -> Refactorer
)

researcher_agent_1 = Agent(
    name="ResearcherAgent",
    model="gemini-2.0-flash",
    description=(
        "Agent to do research about a project from google"
    ),
    instruction=(
        "You are a helpful agent who can explain *only* the purpose given project"
    ),
    tools=[google_search],
    output_key="researcher"
)

parallel_research_agent = ParallelAgent(
    name="ParallelWebResearchAgent",
    sub_agents=[researcher_agent_1, sequential_agent],
    description="Runs multiple research agents in parallel to gather information."
)

merger_agent = LlmAgent(
    name="MergerAgent",
    model="gemini-2.0-flash",
    description=(
        "Merges the Research and code"
    ),
    instruction=("""You just need to join research provided by a parallel model and Code provided by a parallel model 
    with proper indentation and separation between research section and Code section. research:{researcher} code:{
    refactored_code} """),
)
code_pipeline_agent = SequentialAgent(
    name="CodePipelineAgent",
    sub_agents=[parallel_research_agent, merger_agent],
    description="Runs multiple research agents in parallel to gather information."
)

root_agent = code_pipeline_agent
