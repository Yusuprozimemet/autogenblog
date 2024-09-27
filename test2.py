import streamlit as st
import autogen
import os
from datetime import datetime

# Ensure the coding directory exists
if not os.path.exists("coding"):
    os.makedirs("coding")

llm_config = {
    "model": "gpt-4o-mini",
    "api_key": "sk-s64HzGGAq7Sm_dblcr7kf3ZclJ4Sr3tLyLCNw5G0BGT3BlbkFJG6BCNPuwNymr0ropj5-AlICHeCUQbcK_DZrtxOkkgA"
}

writing_tasks = [
    """
    Develop a comprehensive research report about the IT jobs sector using all provided information, including the jobs_trend.png figure and any other supplied figures.
    Focus on the top ten IT jobs.
    For each job:
    1. Retrieve at least 5 relevant skills required.
    2. Provide the average salary range.
    3. List the most common locations for these jobs.
    4. Describe the educational requirements.
    
    Organize the information by creating a table comparing these job requirements.
    
    Additionally, include:
    - Detailed descriptions and analysis of all selected top ten jobs.
    - An in-depth analysis of possible future trends in the IT sector, considering technological advancements and industry shifts.
    - Discussion on the correlation between college degrees and salaries in the IT sector.
    - Insights on how remote work is affecting the IT job market.
    
    Format the report with clear headings, subheadings, and bullet points for readability.
    """
]

# ... (rest of the agent definitions remain the same)
job_assistant = autogen.AssistantAgent(
    name="job_assistant",
    llm_config=llm_config,
)
IT_professional = autogen.AssistantAgent(
    name="IT_professional",
    llm_config=llm_config,
)

writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for your insightful and engaging IT sector and various job requirements.
        You excel at transforming complex concepts into compelling narratives.
        
        Include all metrics provided to you as context in your analysis.
        When responding, only provide the IT jobs report in markdown format directly.
        Do not include markdown language block indicators.
        Only return the final work without any additional comments.
        """
)


export_assistant = autogen.AssistantAgent(
    name="Exporter",
    llm_config=llm_config,
)
# ===

critic = autogen.AssistantAgent(
    name="Critic",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
    system_message="""
        You are a critic. You review the work of the writer and provide constructive 
        feedback to help improve the quality of the content.
    """
)

legal_reviewer = autogen.AssistantAgent(
    name="legal_reviewer",
    llm_config=llm_config,
    system_message="""
        You are a legal reviewer, known for your ability to ensure that content is legally compliant 
        and free from any potential legal issues. 
        Make sure your suggestion is concise (within 3 bullet points), 
        concrete, and to the point.
        Begin the review by stating your role.
    """
)

consistency_reviewer = autogen.AssistantAgent(
    name="consistency_reviewer",
    llm_config=llm_config,
    system_message="""
        You are a consistency reviewer, known for your ability to ensure that the written content is consistent throughout the report. 
        Refer to numbers and data in the report to determine which version should be chosen in case of contradictions. 
        Make sure your suggestion is concise (within 3 bullet points), 
        concrete, and to the point.
        Begin the review by stating your role.
    """
)

textalignment_reviewer = autogen.AssistantAgent(
    name="Text_Alignment_Reviewer",
    llm_config=llm_config,
    system_message="""
        You are a text data alignment reviewer, known for your ability to ensure that the meaning of the written content aligns 
        with the numbers presented in the text. 
        You must ensure that the text clearly describes the numbers without contradictions. 
        Make sure your suggestion is concise (within 3 bullet points), 
        concrete, and to the point.
        Begin the review by stating your role.
    """
)

completion_reviewer = autogen.AssistantAgent(
    name="Completion_Reviewer",
    llm_config=llm_config,
    system_message="""
        You are a content completion reviewer, known for your ability to ensure that IT jobs reports contain all required elements. 
        You verify that the report includes:  
        a description of the different IT jobs, 
        a description of possible future scenarios, a table comparing job trends over the 5 years, 
        and at least one figure. 
        Make sure your suggestion is concise (within 3 bullet points), 
        concrete, and to the point.
        Begin the review by stating your role.
    """
)

meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="""
        You are a meta reviewer. You aggregate and review the feedback from other reviewers 
        and give a final suggestion on the content.
    """
)


def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content.
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''


review_chats = [
    {
        "recipient": legal_reviewer, "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {"summary_prompt":
                         "Return review into a JSON object only:"
                         "{'Reviewer': '', 'Review': ''}.", },
        "max_turns": 1},
    {"recipient": textalignment_reviewer, "message": reflection_message,
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt":
                      "Return review into a JSON object only:"
                      "{'reviewer': '', 'review': ''}", },
     "max_turns": 1},
    {"recipient": consistency_reviewer, "message": reflection_message,
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt":
                      "Return review into a JSON object only:"
                      "{'reviewer': '', 'review': ''}", },
     "max_turns": 1},
    {"recipient": completion_reviewer, "message": reflection_message,
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt":
                      "Return review into a JSON object only:"
                      "{'reviewer': '', 'review': ''}", },
     "max_turns": 1},
    {"recipient": meta_reviewer,
     "message": "Aggregrate feedback from all reviewers and give final suggestions on the writing.",
     "max_turns": 1},
]

critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "coding",
        "use_docker": False,
    },
)

st.title("IT Job Market Analysis")
assets = st.text_input("Enter IT jobs you want to analyze (comma-separated):", "Software Engineer, Data Scientist, DevOps Engineer")
hit_button = st.button('Start Analysis')

if hit_button:
    date_str = datetime.now().strftime("%Y-%m-%d")

    job_search_tasks = [
        f"""Today is {date_str}.
        Analyze the current trends of {assets}, including average salaries, requirements, and geographical distribution.
        1. Start by retrieving the full name of job titles and use these for all future requests.
        2. Prepare a figure of IT jobs trends and save it as 'job_trend.png'. Include:
           * Job requirements
           * Salary ranges
           * Top locations (focus on global trends, with special attention to the Netherlands)
           * Education requirements
        3. Analyze the correlation between college degrees and salaries.
        4. Investigate the impact of remote work on these IT jobs.
        Use web scraping or public datasets. Do not use solutions requiring API keys.
        If data is inconsistent or unavailable, adjust the query and retry.
        Ensure all data is recent (within the last year) and from reputable sources.""",

        f"""Investigate potential future hot IT jobs based on recent news.
        1. Use web scraping to retrieve at least 20 relevant news headlines from reputable tech news sources.
        2. Focus on emerging technologies and industry trends related to {assets}.
        3. Analyze these headlines to identify potential new job roles or skills that may become important.
        4. Create a word cloud image of key terms from these headlines and save it as 'future_trends.png'.
        Do not use solutions requiring API keys. Provide a brief analysis of each trend identified.""",
    ]

    with st.spinner("AI agents are analyzing the IT job market..."):
        chat_results = autogen.initiate_chats(
            [
                {
                    "sender": user_proxy_auto,
                    "recipient": job_assistant,
                    "message": job_search_tasks[0],
                    "silent": False,
                    "summary_method": "reflection_with_llm",
                    "summary_args": {
                        "summary_prompt": "Return the IT jobs and their related requirements, salary ranges, and locations as a JSON object. Include names of all figure files created and the full names of the jobs analyzed.",
                    },
                    "clear_history": False,
                    "carryover": "Ensure all data is properly collected and visualized before terminating. Verify data quality and completeness. Reply TERMINATE when finished."
                },
                {
                    "sender": user_proxy_auto,
                    "recipient": IT_professional,
                    "message": job_search_tasks[1],
                    "silent": False,
                    "summary_method": "reflection_with_llm",
                    "summary_args": {
                        "summary_prompt": "Provide a summary of future IT job trends, including key emerging technologies and skills. Return the result as a JSON object.",
                    },
                    "clear_history": False,
                    "carryover": "Ensure the word cloud is generated and saved. Provide a brief analysis of identified trends. Reply TERMINATE when complete."
                },
                {
                    "sender": critic,
                    "recipient": writer,
                    "message": writing_tasks[0],
                    "carryover": "Ensure the report includes all required elements: job descriptions, future trends, comparative table, and all generated figures. Aim for a comprehensive, well-structured, and insightful report.",
                    "max_turns": 3,
                    "summary_method": "last_msg",
                }
            ]
        )

    st.subheader("IT Job Market Trends")
    st.image("./coding/jobs_trend.png")
    
    st.subheader("Future IT Job Trends")
    st.image("./coding/future_trends.png")
    
    st.subheader("Comprehensive IT Job Market Report")
    st.markdown(chat_results[-1].chat_history[-1]["content"])

    # Option to download the full report
    report_content = chat_results[-1].chat_history[-1]["content"]
    st.download_button(
        label="Download Full Report",
        data=report_content,
        file_name="IT_Job_Market_Analysis.md",
        mime="text/markdown"
    )