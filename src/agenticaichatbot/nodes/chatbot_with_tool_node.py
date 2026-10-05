from src.agenticaichatbot.state.state import State



class ChatbotWithToolNode:
    """
    Chatbot with Tool logic implementation
    
    """

    def __init__(self,model):
        self.llm = model


    def process(self,state:State) -> dict:
        """
        Process the input state and generates a chatbot response with tool integration.
        
        """

        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])

        # Simulate tool-specific logic
        tools_response = f"Tools integration for: {user_input}"
        return {"messages":[llm_response, tools_response]}

    def create_chatbot(self, tools):
        """
         Return a chatbot node function.
        
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State) -> dict:
            """
            Chatbot logic for processing the input state and returning a resposne.
            """
          
            return {"messages":[llm_with_tools.invoke(state['messages'])]}
        # Logic to create and return a chatbot instance with tools
        return chatbot_node