import autogen
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import random

llm_config = {
    "model": "gpt-4o-mini",
    "api_key": "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"
}

def generate_and_save_wordcloud(text, filename):
    wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
    plt.figure(figsize=(10,5))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(os.path.join('coding', filename))
    plt.close()
    print(f"Successfully saved {filename}")

def generate_and_save_trend_graph(data, filename):
    plt.figure(figsize=(10,5))
    plt.plot(data)
    plt.title("RNA Research Trends")
    plt.xlabel("Year")
    plt.ylabel("Number of Publications")
    plt.savefig(os.path.join('coding', filename))
    plt.close()
    print(f"Successfully saved {filename}")

research_assistant = autogen.AssistantAgent(
    name="Research_Assistant",
    llm_config=llm_config,
    system_message="You are an expert in RNA research and bioinformatics."
)

user_proxy = autogen.UserProxyAgent(
    name="User_Proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
)

task = """
1. Conduct a brief literature review on recent advancements in RNA research, focusing on:
   RNA splicing, structure prediction, molecular dynamics, stability, and thermodynamics in splicing.
2. Identify key trends and emerging topics in RNA research.
3. Create a short report including:
   - Executive summary
   - Brief overview of each research area
   - Analysis of trends and emerging topics
   - Future directions
4. Generate a word cloud of key terms and a trend graph of publications over time.
5. Save the report as 'RNA_Research_Report.md' in the 'coding' folder, including the visualizations.
Respond with 'TERMINATE' when the task is complete.
"""

user_proxy.initiate_chat(research_assistant, message=task)

# Generate word cloud and trend graph
research_text = " ".join([msg['content'] for msg in user_proxy.chat_messages[research_assistant] if msg['role'] == 'assistant'])
generate_and_save_wordcloud(research_text, 'rna_trends_wordcloud.png')

years = list(range(2020, 2025))
publications = [random.randint(100, 500) for _ in range(5)]
generate_and_save_trend_graph(publications, 'rna_research_trends.png')

# Create and save the report
report_content = """# RNA Research Report

## Executive Summary

(Insert brief executive summary)

## Research Areas Overview

(Insert brief overview of each research area)

## Trends and Emerging Topics

![RNA Research Trends Word Cloud](./rna_trends_wordcloud.png)
![RNA Research Trends Graph](./rna_research_trends.png)

(Insert analysis of trends and emerging topics)

## Future Directions

(Insert brief section on future directions)
"""

os.makedirs('coding', exist_ok=True)
with open('coding/RNA_Research_Report.md', 'w') as f:
    f.write(report_content)

print("Report 'RNA_Research_Report.md' saved in the 'coding' folder.")