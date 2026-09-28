from duckduckgo_search import DDGS
from crewai.tools import tool

@tool("duckduckgo_search")
def search_tool(query: str) -> str:
    """Search the internet for professor details, university departments, and contact info using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if not results:
                return "No relevant information found."
            # Clean and concise summary for the LLM
            formatted_results = []
            for r in results:
                title = r.get("title", "")
                body = r.get("body", "")
                href = r.get("href", "")
                formatted_results.append(f"Title: {title}\nSnippet: {body}\nURL: {href}")
            return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error occurred during search: {str(e)}"
