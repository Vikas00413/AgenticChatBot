
from typing import Any, List
from typing_extensions import NotRequired, TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated


class State(TypedDict):
    """
    Represent the structure of the state graph in graph
    """
    messages: Annotated[List,add_messages]
    frequency: NotRequired[str]
    news_data: NotRequired[list[dict[str, Any]]]
    summary: NotRequired[str]
    filename: NotRequired[str]