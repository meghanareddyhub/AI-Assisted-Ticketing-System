import streamlit as st
import ai_chat

st.set_page_config(page_title="AI Chat")

st.title("🤖 AI Ticket Assistant")
st.caption("Ask about ticket counts, statuses, or assignees — answers use live ticket data.")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask a question about tickets...")

if question:
    st.session_state.chat_messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Checking ticket data..."):
            try:
                answer = ai_chat.answer_question(question)
            except Exception as e:
                answer = f"Something went wrong answering that: {e}"
        st.markdown(answer)

    st.session_state.chat_messages.append({"role": "assistant", "content": answer})