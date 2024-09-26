import autogen
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random
import json

llm_config = {
    "model": "gpt-4o-mini",
    "api_key": "sk-s64HzGGAq7Sm_dblcr7kf3ZclJ4Sr3tLyLCNw5G0BGT3BlbkFJG6BCNPuwNymr0ropj5-AlICHeCUQbcK_DZrtxOkkgA"
}

# Ensure the 'coding' folder exists
os.makedirs('coding', exist_ok=True)

# Research and writing tasks
research_tasks = [
    """Today is Thursday, September 26, 2024.
    Conduct a comprehensive literature review on recent advancements in RNA research.
    Focus on the following areas:
    1. RNA splicing
    2. RNA structure prediction and modeling
    3. RNA molecular dynamics
    4. RNA stability
    5. RNA thermodynamics in splicing
    For each area, identify key papers, researchers, and institutions leading the field.
    Retrieve at least 10 relevant papers for each area, published within the last 3 years.
    Do not use a solution that requires an API key."""
]

writing_tasks = [
    """Develop a comprehensive RNA research report using all information provided. Include:
    1. An executive summary of the current state of RNA research
    2. Detailed sections on each of the five focus areas, highlighting key findings and breakthroughs
    3. Analysis of trends and emerging topics in RNA research
    4. Visualizations created during the research process, include the rna_trends_wordcloud.png
    5. A section on future directions and potential applications of RNA research
    6. A bibliography of all papers referenced in the report
    Ensure that the report is well-structured, engaging, and accessible to a scientific audience with a background in molecular biology."""
]

exporting_task = [
    """Save the report and only the report to a .md file using a python script."""]

# Agent definitions
research_assistant = autogen.AssistantAgent(
    name="Research_Assistant",
    llm_config=llm_config,
    system_message="You are an expert in RNA research and bioinformatics, "
                   "capable of conducting thorough literature reviews and data analysis."
)

writer = autogen.AssistantAgent(
    name="Scientific_Writer",
    llm_config=llm_config,
    system_message="You are a professional scientific writer, known for "
                   "producing clear, concise, and engaging research reports. "
                   "You excel at synthesizing complex scientific information "
                   "into coherent narratives."
)

export_assistant = autogen.AssistantAgent(
    name="Exporter",
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="You are a critic with expertise in RNA research. "
                   "You review scientific reports and provide constructive feedback "
                   "to improve their accuracy, clarity, and completeness. "
                   "After 3 iterations of review and revision, you must conclude the process "
                   "and instruct the writer to provide the final report."
)

scientific_reviewer = autogen.AssistantAgent(
    name="Scientific_Reviewer",
    llm_config=llm_config,
    system_message="You are a scientific reviewer with deep knowledge of RNA biology. "
                   "Ensure that the report accurately represents the current state of RNA research, "
                   "includes all relevant breakthrough discoveries, and correctly interprets the data."
)

consistency_reviewer = autogen.AssistantAgent(
    name="Consistency_Reviewer",
    llm_config=llm_config,
    system_message="You are a consistency reviewer, ensuring that the scientific report "
                   "maintains a coherent narrative and consistent terminology throughout. "
                   "Check for any contradictions or inconsistencies in the presented information."
)

meta_reviewer = autogen.AssistantAgent(
    name="Meta_Reviewer",
    llm_config=llm_config,
    system_message="You are a meta reviewer, aggregating and synthesizing feedback "
                   "from other reviewers to provide final suggestions for improving the RNA research report."
)

# Review process


def reflection_message(recipient, messages, sender, config):
    return f'''Review the following content of the RNA research report.
            \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}'''


review_chats = [
    {
        "recipient": scientific_reviewer, "message": reflection_message,
        "summary_method": "reflection_with_llm",
        "summary_args": {"summary_prompt":
                         "Return review into a JSON object only:"
                         "{'Reviewer': '', 'Review': ''}.", },
        "max_turns": 1},
    {"recipient": consistency_reviewer, "message": reflection_message,
     "summary_method": "reflection_with_llm",
     "summary_args": {"summary_prompt":
                      "Return review into a JSON object only:"
                      "{'reviewer': '', 'review': ''}", },
     "max_turns": 1},
    {"recipient": meta_reviewer,
     "message": "Aggregate feedback from all reviewers and give final suggestions on the RNA research report.",
     "max_turns": 1},
]

critic.register_nested_chats(
    review_chats,
    trigger=writer,
)

# User proxy agent
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

max_turns = 10
# Initiate chats
chat_results = autogen.initiate_chats(
    [
        {
            "sender": user_proxy_auto,
            "recipient": research_assistant,
            "message": research_tasks[0],
            "silent": False,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Summarize the key findings from the literature review for each RNA research area into a JSON object.",
            },
            "clear_history": False,
            "carryover": "Ensure all research areas are covered comprehensively. Reply TERMINATE when the literature review is complete.",
            "max_turns": max_turns
        },
        {
            "sender": user_proxy_auto,
            "recipient": research_assistant,
            "message": "Based on the literature review, create visualizations for RNA research trends. Save them as 'rna_trends_wordcloud.png' and 'rna_research_trends.png'.",
            "silent": False,
            "summary_method": "reflection_with_llm",
            "summary_args": {
                "summary_prompt": "Summarize the trends and patterns in RNA research as a JSON object. Include names of visualization files created.",
            },
            "clear_history": False,
            "carryover": "Ensure all visualizations are created and saved. Reply TERMINATE when the analysis is complete.",
            "max_turns": max_turns
        },
        {
            "sender": critic,
            "recipient": writer,
            "message": writing_tasks[0],
            "carryover": "Include all visualizations and ensure comprehensive coverage of all research areas in the RNA research report. After 3 iterations, provide the final report.",
            "max_turns": 3,
            "summary_method": "last_msg",
        },
        {
            "sender": user_proxy_auto,
            "recipient": export_assistant,
            "message": exporting_task[0],
            "carryover": "Wait for confirmation of code execution before terminating the conversation. Reply TERMINATE in the end when everything is done.",
            "max_turns": max_turns
        }
    ]
)

# Extract research text from chat results
research_text = ""
for result in chat_results:
    if isinstance(result, autogen.ChatResult):
        for message in result.messages:
            if message['role'] == 'assistant':
                research_text += message['content'] + " "

# Create word cloud


def create_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400,
                          background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig('coding/rna_trends_wordcloud.png')
    plt.close()


create_wordcloud(research_text)

# Create research trends plot (placeholder function)


def create_research_trends_plot():
    # This is a placeholder. In a real scenario, you'd analyze the research data to create this plot.
    trends = {'RNA splicing': random.randint(50, 100),
              'RNA structure prediction': random.randint(50, 100),
              'RNA molecular dynamics': random.randint(50, 100),
              'RNA stability': random.randint(50, 100),
              'RNA thermodynamics': random.randint(50, 100)}

    plt.figure(figsize=(10, 6))
    plt.bar(trends.keys(), trends.values())
    plt.title('RNA Research Trends')
    plt.xlabel('Research Areas')
    plt.ylabel('Research Activity (arbitrary units)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('coding/rna_research_trends.png')
    plt.close()


create_research_trends_plot()

# Save the report as a .md file
with open('coding/rna_research_report.md', 'w', encoding='utf-8') as f:
    f.write(research_text)

print("RNA research report generation complete. Check the 'coding' folder for output files.")
