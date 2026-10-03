import streamlit as st
from src.agenticaichatbot.ui.streamlit.loadui import LoadStreamlitUI


def load_langgraph_agentic_ai_app():
    """
    Loads and run the Langgraph AgenticAI application with Streamlit UI.
    This function initializes the UI, handles user input, configures the LLm model,
    set up the graph based on the selected use acse, and display the output while
    implementing exception handling for robustness.
    """

    ## Load UI
    ui= LoadStreamlitUI()
    user_input= ui.load_streamlit_ui()

    if not user_input:
        st.error(" Error , Failed load user input from the UI.")
        return


    user_message = st.chat_input('Enter Your Message:')

    # if user_message :
    #     try :
    #         # config LLM
    #         obj_llm_config = GroqLLM(user_controls_input=user_input)
    #         model= obj_llm_config.get_llm_model()

    #         if not model:
    #             st.error('Erroe : LLM model could not be initilized')

    #         usecase = user_input.get('selected_usecase')

    #         if not usecase:
    #             st.error('Error No use case slected.')
    #             return
    