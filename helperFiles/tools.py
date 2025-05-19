import arxiv
from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

def search_arxiv_papers(query: str, max_results: int = 5, sort_by: str = "relevance") -> dict:
    """
    Searches for academic papers on arXiv based on a query.

    Args:
        query (str): The search query (keywords, title, author, etc.).
        max_results (int, optional): The maximum number of results to return. Defaults to 5.
        sort_by (str, optional): How to sort results. Options: "relevance", "lastUpdatedDate", "submittedDate".
                                 Defaults to "relevance".

    Returns:
        dict: A dictionary containing the status and either a list of paper details or an error message.
              Each paper detail includes title, authors, summary, arXiv ID, PDF link, and published date.
    """
    client = arxiv.Client()
    if not query or not query.strip():
        return {
            "status": "error",
            "error_message": "Query cannot be empty.",
        }

    try:
        if sort_by.lower() == "lastupdateddate":
            sort_criterion = arxiv.SortCriterion.LastUpdatedDate
        elif sort_by.lower() == "submitteddate":
            sort_criterion = arxiv.SortCriterion.SubmittedDate
        else:  # Default to relevance
            sort_criterion = arxiv.SortCriterion.Relevance

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_criterion
        )

        results = []

        for result in client.results(search):
            authors = [author.name for author in result.authors]
            results.append({
                "title": result.title,
                "authors": ", ".join(authors),
                "summary": result.summary,
                "arxiv_id": result.entry_id.split('/')[-1],  # Get just the ID part
                "pdf_link": result.pdf_url,
                "published_date": result.published.strftime("%Y-%m-%d %H:%M:%S UTC"),  # Format datetime
                "arxiv_page_url": result.entry_id
            })

        if not results:
            return {
                "status": "success",  # Successful query, but no results found
                "report": f"No papers found for query: '{query}' with the given criteria.",
                "papers": []
            }

        return {
            "status": "success",
            "report": f"Found {len(results)} papers matching your query.",
            "papers": results,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while searching arXiv: {str(e)}",
        }

summary_agent = Agent(
    model="gemini-2.0-flash",
    name="summary_agent",
    instruction="""You are an expert summarizer. Please read the following text and provide a concise summary.""",
    description="Agent to summarize text",
)

summerising_AgentTool = AgentTool(summary_agent)