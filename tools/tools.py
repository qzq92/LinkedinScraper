# Search API optimized for LLM and RAG. Limit to 1000Apis call/month. Refer to https://docs.tavily.com/docs/tavily-api/introduction. 
from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_via_tavily(name:str):
    """Searches for Linkedin or X profile page.

    Args:
        name (str): String to be parsed as search value.
    """
    search = TavilySearchResults()
    res = search.run(f"{name}")

    return res[0]["url"]