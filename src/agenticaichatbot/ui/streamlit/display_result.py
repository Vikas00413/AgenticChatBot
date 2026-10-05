import streamlit as st
import streamlit.components.v1 as components
from langchain_core.messages import AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase=usecase
        self.graph=graph
        self.user_message=user_message

    def display_result_on_ui(self):
        if self.usecase not in ("Basic Chatbot", "Chatbot With Web"):
            raise ValueError(f"Unsupported chat use case: {self.usecase}")

        chat_history = st.session_state.setdefault("chat_history", [])
        chat_history.append({"role": "user", "content": self.user_message})

        with st.chat_message("user"):
            st.write(self.user_message)

        messages = [
            (message["role"], message["content"])
            for message in chat_history
        ]
        tool_statuses = {}
        assistant_message = None

        with st.chat_message("assistant"):
            for update in self.graph.stream(
                {"messages": messages},
                stream_mode="updates",
            ):
                for node_update in update.values():
                    for message in node_update.get("messages", []):
                        if isinstance(message, AIMessage) and message.tool_calls:
                            for tool_call in message.tool_calls:
                                tool_name = tool_call["name"]
                                status = st.status(
                                    f"Tool started: {tool_name}",
                                    expanded=True,
                                )
                                status.write("Tool is running.")
                                tool_statuses[tool_call["id"]] = status
                        elif isinstance(message, ToolMessage):
                            status = tool_statuses.get(message.tool_call_id)
                            if status is None:
                                status = st.status(
                                    f"Tool finished: {message.name or 'tool'}",
                                    expanded=True,
                                )
                            status.write("Tool result:")
                            status.write(message.content)
                            status.update(
                                label=f"Tool finished: {message.name or 'tool'}",
                                state="complete",
                            )
                        elif isinstance(message, AIMessage):
                            assistant_message = message

            if assistant_message is None:
                raise RuntimeError("The graph completed without an assistant message.")

            st.write(assistant_message.content)

        chat_history.append(
            {"role": "assistant", "content": assistant_message.content}
        )

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

        