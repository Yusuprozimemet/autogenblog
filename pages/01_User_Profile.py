import streamlit as st
import random

st.set_page_config(page_title="User Profile", page_icon="👤", layout="wide")

st.title("👤 User Profile")

# Initialize session state for user profile
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "",
        "email": "",
        "bio": "",
        "favorite_topics": [],
        "chat_style": "Casual"
    }

# User information form
with st.form("user_profile_form"):
    st.header("Personal Information")
    name = st.text_input("Name", st.session_state.user_profile["name"])
    email = st.text_input("Email", st.session_state.user_profile["email"])
    bio = st.text_area("Bio", st.session_state.user_profile["bio"])
    
    st.header("Chat Preferences")
    favorite_topics = st.multiselect(
        "Favorite Topics",
        ["Technology", "Science", "Arts", "Sports", "Politics", "History", "Philosophy"],
        st.session_state.user_profile["favorite_topics"]
    )
    chat_style = st.selectbox(
        "Preferred Chat Style",
        ["Casual", "Formal", "Technical", "Creative"],
        index=["Casual", "Formal", "Technical", "Creative"].index(st.session_state.user_profile["chat_style"])
    )
    
    submitted = st.form_submit_button("Save Profile")
    if submitted:
        st.session_state.user_profile = {
            "name": name,
            "email": email,
            "bio": bio,
            "favorite_topics": favorite_topics,
            "chat_style": chat_style
        }
        st.success("Profile updated successfully!")

# Display current profile
st.header("Current Profile")
st.write(f"**Name:** {st.session_state.user_profile['name']}")
st.write(f"**Email:** {st.session_state.user_profile['email']}")
st.write(f"**Bio:** {st.session_state.user_profile['bio']}")
st.write(f"**Favorite Topics:** {', '.join(st.session_state.user_profile['favorite_topics'])}")
st.write(f"**Preferred Chat Style:** {st.session_state.user_profile['chat_style']}")

# Fun feature: Random chat prompt based on user's favorite topics
if st.session_state.user_profile["favorite_topics"]:
    st.header("Conversation Starter")
    topic = random.choice(st.session_state.user_profile["favorite_topics"])
    prompts = {
        "Technology": "What's the most exciting tech innovation you've heard about recently?",
        "Science": "If you could instantly become an expert in one scientific field, which would you choose?",
        "Arts": "What's your favorite form of artistic expression and why?",
        "Sports": "If you could be a professional athlete, which sport would you choose?",
        "Politics": "What's one political issue you think doesn't get enough attention?",
        "History": "If you could witness any historical event, which one would it be?",
        "Philosophy": "What's a philosophical question that you often ponder?"
    }
    st.info(f"Here's a conversation starter about {topic}: {prompts.get(topic, 'Tell me something interesting about ' + topic)}")

# Footer
st.markdown("---")
st.markdown("Customize your profile to enhance your chat experience!")