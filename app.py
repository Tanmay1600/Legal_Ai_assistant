import streamlit as st
from model import get_answer

st.set_page_config(page_title="Legal AI Assistant", layout="centered")

st.title("⚖️ Legal AI Assistant")
st.write("Ask anything about Indian Law")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
query = st.chat_input("Type your question...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.write(query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer = get_answer(query)
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})