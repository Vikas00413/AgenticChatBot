import streamlit as st
import streamlit.components.v1 as components
from langchain_core.messages import AIMessage, ToolMessage

class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase=usecase
        self.graph=graph
        self.user_message=user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        if usecase not in ("Basic Chatbot", "Chatbot With Web", "AI News"):
            raise ValueError(f"Unsupported chat use case: {self.usecase}")

        chat_history = st.session_state.setdefault("chat_history", [])
        chat_history.append({"role": "user", "content": user_message})

        with st.chat_message("user"):
            st.write(user_message)

        messages = [
            (message["role"], message["content"])
            for message in chat_history
        ]

        if usecase == "Basic Chatbot":
            assistant_message = None

            with st.chat_message("assistant"):
                for update in graph.stream(
                    {"messages": messages},
                    stream_mode="updates",
                ):
                    for node_update in update.values():
                        for message in node_update.get("messages", []):
                            if isinstance(message, AIMessage):
                                assistant_message = message

                if assistant_message is None:
                    raise RuntimeError("The graph completed without an assistant message.")

                assistant_content = assistant_message.content
                st.write(assistant_content)

        elif usecase == "Chatbot With Web":
            assistant_message = None
            tool_statuses = {}

            with st.chat_message("assistant"):
                for update in graph.stream(
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

                assistant_content = assistant_message.content
                st.write(assistant_content)

        elif usecase == "AI News":
            frequency = st.session_state.get("time_frame", user_message).lower()
            with st.spinner("Fetching and summarizing AI news..."):
                result = graph.invoke({"messages": [("user", frequency)]})
                news_filename = result.get("filename")

                if not news_filename:
                    raise RuntimeError("The AI News graph completed without saving a result.")

                try:
                    with open(news_filename, encoding="utf-8") as result_file:
                        assistant_content = result_file.read()
                except FileNotFoundError:
                    st.error(f"AI News result file was not found: {news_filename}")
                    return

                with st.chat_message("assistant"):
                    st.markdown(assistant_content)

        chat_history.append(
            {"role": "assistant", "content": assistant_content}
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

        