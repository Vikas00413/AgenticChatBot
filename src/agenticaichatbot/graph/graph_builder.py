from langgraph.graph import StateGraph ,START, END

from agenticaichatbot.tools.search_tool import create_tool_node, get_tools
from src.agenticaichatbot.state.state import State
from src.agenticaichatbot.nodes.basic_chatbot_node import BasicChatbotNode
from langgraph.prebuilt import ToolNode,tools_condition
from src.agenticaichatbot.nodes.chatbot_with_tool_node import ChatbotWithToolNode
from src.agenticaichatbot.nodes.ai_news_node import AINewsNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)



    def chatbot_qith_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph thet includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot node with these tools, 
        capabilitiues, and sets up conditional and direct edge between nodes.
        The chatbot node is set as the entry point.
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)

        ## Define llm
        llm=self.llm

        ## Define chatbot node
        obj_chatbot_with_node = ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
        ## Add The node
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        ## Define condtional and direct edge

        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge('tools',"chatbot")
        self.graph_builder.add_edge('chatbot',END)

    def ai_news_build_graph(self):
        """
        Builds a graph for the AI News use case.
        This method creates a graph that includes a chatbot node and a tool node 
        specifically designed for fetching AI news. It sets up the necessary nodes 
        and edges to facilitate the flow of information between the chatbot and the tool.
        The chatbot node is set as the entry point.
        """
        ai_news_node=AINewsNode(self.llm)

        ## Added Nodes
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
       
        ## Add edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)
   


 

    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        if usecase == "Chatbot With Web":
            self.chatbot_qith_tools_build_graph()
        if usecase == "AI News":
            self.ai_news_build_graph()

        return self.graph_builder.compile()





