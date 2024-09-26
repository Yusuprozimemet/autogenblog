import streamlit as st

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = 0

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.chat_history = []
    st.success("Chat history cleared!")

def start_new_chat():
    st.session_state.messages = []
    st.session_state.current_chat_id += 1
    st.success("New chat started!")

def add_message_to_history(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.chat_history.append({
        "chat_id": st.session_state.current_chat_id,
        "role": role,
        "content": content
    })

def get_current_chat_messages():
    return [msg for msg in st.session_state.chat_history if msg["chat_id"] == st.session_state.current_chat_id]

def get_chat_list():
    chat_ids = set(msg["chat_id"] for msg in st.session_state.chat_history)
    return sorted(list(chat_ids), reverse=True)