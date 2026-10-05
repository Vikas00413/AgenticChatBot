from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode

def get_tools():
    """
    Returns a list of tools to be used in the chatbot graph.
    Currently, it includes the TavilySearchResults tool for web search capabilities.
    """
    tools = [TavilySearchResults(max_results=2)]
    return tools

def create_tool_node(tools):
    """
    Creates a ToolNode using the provided tools.
    This node can be integrated into the chatbot graph to enable tool-based interactions.
    """
    tool_node = ToolNode(tools=tools)
    return tool_node