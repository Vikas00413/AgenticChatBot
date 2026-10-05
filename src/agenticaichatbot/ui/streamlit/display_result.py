import streamlit as st
import streamlit.components.v1 as components

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase=usecase
        self.graph=graph
        self.user_message=user_message

    def display_result_on_ui(self):
        usecase=self.usecase
        graph=self.graph
        user_message=self.user_message
        if usecase == 'Basic Chatbot' :
            chat_history = st.session_state.setdefault("chat_history", [])
            chat_history.append({"role": "user", "content": user_message})

            with st.chat_message("user"):
                st.write(user_message)

            messages = [
                (message["role"], message["content"])
                for message in chat_history
            ]
            result = graph.invoke({"messages": messages})
            assistant_message = result["messages"][-1]
            chat_history.append(
                {"role": "assistant", "content": assistant_message.content}
            )

            with st.chat_message("assistant"):
                st.write(assistant_message.content)

            components.html(
                """
                <script>
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            window.frameElement?.scrollIntoView({
                                behavior: "smooth",
                                block: "end"
                            });
                        });
                    });
                </script>
                """,
                height=0,
            )

        