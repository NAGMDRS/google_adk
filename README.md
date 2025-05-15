# Google ADK Repository Overview

This repository contains AI agents built using Google's Agent Development Kit (ADK). It includes two primary agent systems:

- **Code Pipeline Agent**: A multi-stage system that generates, reviews, and refactors code based on user's project requirements.
- **ResearcherAgent**: An agent that searches and summarizes academic papers from ArXiv.

Both agents utilize Google's Gemini 2.0 Flash model and are supported by shared helper tools for tasks like ArXiv searches and text summarization.

---

## 📁 Repository Structure

```
google_adk/
├── agent/
│   ├── __init__.py
│   └── agent.py              # Code Pipeline Agent
├── researchAgent/
│   ├── __init__.py
│   └── agent.py              # ResearcherAgent
└── helperFiles/
    └── tools.py              # ArXiv Search & Summarization Tools
```

---

## 🧠 Key Components

### Code Pipeline Agent

A pipeline for generating, reviewing, and refactoring code. It integrates research capabilities with a sequential code generation process.

**Location:** `agent/agent.py:120-124`

#### Architecture

The Code Pipeline Agent includes multiple specialized sub-agents:

- **Prompt Writer Agent**:  
  Creates prompts for code generation based on user requirements  
  `agent.py:4-12`

- **Code Writer Agent**:  
  Generates initial Python code based on the prompt  
  `agent.py:14-26`

- **Code Reviewer Agent**:  
  Reviews generated code for correctness, readability, efficiency, and best practices  
  `agent.py:29-54`

- **Code Refactorer Agent**:  
  Refactors code based on review comments  
  `agent.py:57-82`

- **Sequential Agent**:  
  Orchestrates the sequential execution of the above agents  
  `agent.py:84-89`

- **Researcher Agent**:  
  Performs research using Google Search  
  `agent.py:91-102`

- **Parallel Research Agent**:  
  Runs research and code generation in parallel  
  `agent.py:104-108`

- **Merger Agent**:  
  Combines research and code into a final output  
  `agent.py:110-119`

#### Workflow

1. User provides a project description
2. Two parallel processes are initiated:
   - Research using Google Search
   - Code generation through a sequential pipeline:
     - Prompt generation
     - Code writing
     - Code reviewing
     - Code refactoring
3. Results from both processes are merged
4. Final output containing research and code is returned to the user

---

### ResearcherAgent

The ResearcherAgent searches and summarizes academic papers from ArXiv, helping users quickly gather relevant research insights.

**Location:** `researchAgent/agent.py:10-22`

#### Architecture

- **Name**: `ResearcherAgent`
- **Model**: Gemini 2.0 Flash
- **Description**: "Agent to do research about a project from Arxiv"
- **Tools**:
  - `search_arxiv_papers`: Searches ArXiv for relevant papers
  - `summerizing_AgentTool`: Summarizes paper abstracts
  - `load_memory`: Accesses previously saved results

The agent runs using a `Runner` with in-memory session and memory services.  
`agent.py:24-32`

#### Workflow

1. User submits a research query
2. Agent checks if the query exists in memory
3. If found, returns previous results
4. If not, searches ArXiv and summarizes papers
5. Saves query and results to memory
6. Returns response to user

---

## 🛠️ Helper Components

Shared tools are available in the `helperFiles` directory:

- **ArXiv Search Tool**:  
  Searches for academic papers on ArXiv based on a query  
  `tools.py:5-71`

- **Summarization Agent Tool**:  
  Summarizes text using a dedicated agent  
  `tools.py:73-80`

---

## 🚀 Getting Started

1. Ensure you have access to Google's Agent Development Kit (ADK)
2. Install the required dependencies
3. Choose the appropriate agent for your task:
   - Use the **Code Pipeline Agent** for code generation tasks
   - Use the **ResearcherAgent** for academic research tasks
4. Use adk web in cmd (or) Use adk run <Agent-name>

---

## 📦 Dependencies

- Google ADK  
- ArXiv Python client  
- Google Gemini 2.0 Flash model
