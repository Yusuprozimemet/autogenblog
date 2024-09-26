import streamlit as st
from openai import OpenAI
import time
from styles.main import load_css
from functions.utils import initialize_session_state, clear_chat_history, start_new_chat, add_message_to_history, get_current_chat_messages, get_chat_list

# Set page config as the first Streamlit command
st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="wide")

# Load CSS
st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state
initialize_session_state()

# LLM configuration
llm_config = {
    "model": "gpt-4o-mini",
    "api_key": "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"
}

# Initialize OpenAI client
client = OpenAI(api_key=llm_config["api_key"])

# Sidebar for app configuration
st.sidebar.title("Chat Configuration")

# Create two columns for buttons
col1, col2 = st.sidebar.columns(2)

# Remove the column layout
if col1.button("New 💬"):
    start_new_chat()
    st.rerun()

if col2.button("clear 🗑️"):
    clear_chat_history()
    st.rerun()

# Display chat history in sidebar
st.sidebar.subheader("Chat History")
chat_list = get_chat_list()

for chat_id in chat_list:
    # Get the first message of this chat
    first_message = next((msg for msg in st.session_state.chat_history if msg["chat_id"] == chat_id), None)
    
    if first_message:
        # Extract the first 30 characters of the content (or less if it's shorter)
        preview = first_message["content"][:30] + "..." if len(first_message["content"]) > 30 else first_message["content"]
        
        # Create a button with the preview text
        if st.sidebar.button(f"{preview}", key=f"chat_{chat_id}"):
            st.session_state.current_chat_id = chat_id
            st.rerun()

# Main chat interface
st.title("🤖 AI Chat Assistant")

# Display current chat
current_chat = get_current_chat_messages()
for message in current_chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat history
    add_message_to_history("user", user_input)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Show a spinner while waiting for the AI response
    with st.spinner("AI is thinking..."):
        # Generate AI response
        response = client.chat.completions.create(
            model=llm_config["model"],
            messages=st.session_state.messages,
            temperature=0.7,  # Fixed temperature
            max_tokens=1000    # Fixed max tokens
        )
    
    # Extract AI response
    ai_response = response.choices[0].message.content
    
    # Add AI response to chat history
    add_message_to_history("assistant", ai_response)
    
    # Display AI response with a typing effect
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in ai_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Rerun the app to update the chat history in the sidebar
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Powered by OpenAI GPT-4o-mini")