def load_css():
    return """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    
    .stTextInput > div > div > input {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px 15px;
        font-size: 16px;
    }
    
  .stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 15px;
    padding: 6px 12px;
    font-size: 12px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    background-color: #45a049;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    transform: translateY(-2px);
}
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: flex-start;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .chat-message.user {
        background-color: #e6f3ff;
        color: #000000;
        margin-left: 20%;
    }
    
    .chat-message.assistant {
        background-color: #ffffff;
        color: #000000;
        margin-right: 20%;
    }
    
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 10px;
    }
    
    .chat-message .message {
        flex-grow: 1;
    }
    
    .stMarkdown {
        font-size: 16px;
        line-height: 1.5;
    }
    
    .stMarkdown p {
        margin-bottom: 10px;
    }
    
    .stSubheader {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #333;
    }
    
    .stSpinner {
        text-align: center;
        padding: 20px;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        font-size: 14px;
        color: #666;
    }
    </style>
    """