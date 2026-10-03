
from typing_extensions import TypedDict,List
from langgraph.graph.message import add_messages
from typing import Annotated


class State(TypedDict):
    """
    Represent the strructure of the state graph in graph
    """
    messages: Annotated[List,add_messages]