import streamlit as st
import os


from src.agenticaichatbot.ui.uiconfigfile import Config


class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls={}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="👤" +self.config.get_page_title() , layout='wide')
        st.header("" +self.config.get_page_title())

        with st.sidebar:

            llm_options = self.config.get_llm_options()
            usecase_options= self.config.get_use_options()

            ## LLm selctions
            self.user_controls['selected_llm'] = st.selectbox("Select LLM", llm_options)

            if self.user_controls['selected_llm'] == 'OPENAI' :
                ## Model selection
                model_options = self.config.get_openai_model_options()
                self.user_controls['selected_openai_model'] = st.selectbox("Select Model", model_options)
                api_key = st.text_input("API KEY", type='password')
                st.session_state["OPENAI_API_KEY"] = api_key
                self.user_controls['OPENAI_API_KEY'] = api_key
                
                if not self.user_controls['OPENAI_API_KEY'] :
                    st.warning("⚠️ Please Enter your OpenAI API KEY , Please check https://platform.openai.com/api-keys")

            ## Usecase selection
            self.user_controls['selected_usecase']=st.selectbox('Select Usecases', usecase_options)

        return self.user_controls


            