import streamlit as st
import autogen

llm_config = {
    "model": "gpt-4o-mini",
    "api_key": "sk-s64HzGGAq7Sm_dblcr7kf3ZclJ4Sr3tLyLCNw5G0BGT3BlbkFJG6BCNPuwNymr0ropj5-AlICHeCUQbcK_DZrtxOkkgA"
}


writing_tasks = [
    """
    Develop a comprehensive RNA research report using all provided information. 
    The report should include the research_trend.png figure, as well as any other figures supplied.
    
    Focus on the following key areas:
    1. RNA splicing
    2. RNA structure prediction and modeling
    3. RNA molecular dynamics
    4. RNA stability
    5. RNA thermodynamics in splicing
    
    For each area, retrieve at least 10 relevant research papers published within the last 3 years.
    Organize the information by creating a table comparing these RNA research papers.
    
    Additionally, include:
    - Comments and descriptions of all selected papers.
    - An analysis of possible future research scenarios.
    """
]


RNA_research_assistant = autogen.AssistantAgent(
    name="RNA_research_assistant",
    llm_config=llm_config,
)
Professor_in_bioinformatics = autogen.AssistantAgent(
    name="Professor_in_bioinformatics",
    llm_config=llm_config,
)

writer = autogen.AssistantAgent(
    name="writer",
    llm_config=llm_config,
    system_message="""
        You are a professional writer, known for your insightful and engaging RNA research reports.
        You excel at transforming complex concepts into compelling narratives.
        
        Include all metrics provided to you as context in your analysis.
        When responding, only provide the RNA research report in markdown format directly.
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
        You are a content completion reviewer, known for your ability to ensure that RNA research reports contain all required elements. 
        You verify that the report includes: a paper on each of the five topics, 
        a description of the different RNA research methods, 
        a description of possible future scenarios, a table comparing research trends over the years, 
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

# ===

user_proxy_auto = autogen.UserProxyAgent(
    name="User_Proxy_Auto",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and x.get(
        "content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "coding",
        "use_docker": False,
    },
)

assets = st.text_input("Assets you want to analyze (provide the tickers)?")
hit_button = st.button('Start analysis')

if hit_button is True:

    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")

    rna_research_tasks = [
        f"""Today is the {date_str}.
        What are the current RNA reseach field related to {assets}, and how is the new breakthrough over the past 1 year?
        Start by retrieving the full name of each research paper and use it for all future requests.
        Prepare a figure of RNA research trend by these papers and save it to a file named research_trend.png. Include information about, if applicable:
        * Research topic
        * Methods
        * relation with AI
        * Practical usage in future theraputics
        * location of the research
        * name of the researchers
        * Analyze the correlation between the AI and research topic
        Do not use a solution that requires an API key.
        If some of the data does not makes sense, such as there is no information, change the query and re-try.""",

        """Investigate possible reasons of the RNA research related  news headlines from Bing News or Google Search. Retrieve news headlines using python and return them. Use the full name research to retrieve headlines. Retrieve at least 10 headlines per research. Do not use a solution that requires an API key. Do not perform a sentiment analysis.""",
    ]

    with st.spinner("Agents working on the analysis...."):
        chat_results = autogen.initiate_chats(
            [
                {
                    "sender": user_proxy_auto,
                    "recipient": RNA_research_assistant,
                    "message": rna_research_tasks[0],
                    "silent": False,
                    "summary_method": "reflection_with_llm",
                    "summary_args": {
                        "summary_prompt": "Return the RNA research topics, their related high impacted papers"
                        "into a JSON object only. Provide the name of all figure files created. Provide the full name of research.",
                    },
                    "clear_history": False,
                    "carryover": "Wait for confirmation of code execution before terminating the conversation. Verify that the data is not completely composed of NaN values. Reply TERMINATE in the end when everything is done."
                },
                {
                    "sender": user_proxy_auto,
                    "recipient": Professor_in_bioinformatics,
                    "message": rna_research_tasks[1],
                    "silent": False,
                    "summary_method": "reflection_with_llm",
                    "summary_args": {
                        "summary_prompt": "Provide the news headlines as a paragraph for each research, be precise but do not consider news events that are vague, return the result as a JSON object only.",
                    },
                    "clear_history": False,
                    "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done."
                },
                {
                    "sender": critic,
                    "recipient": writer,
                    "message": writing_tasks[0],
                    "carryover": "I want to include a figure and a table of the provided data in the RNA research report.",
                    "max_turns": 2,
                    "summary_method": "last_msg",
                }
            ]
        )

    st.image("./coding/research_trend.png")
    st.markdown(chat_results[-1].chat_history[-1]["content"])
