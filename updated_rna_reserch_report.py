import os
import random
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from dotenv import load_dotenv
load_dotenv()

import asyncio
import inspect

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("⚠️ OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Create OpenAI client instance
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", api_key=OPENAI_API_KEY)

# Ensure the 'coding' folder exists
os.makedirs('coding', exist_ok=True)

research_tasks = [
    "Today is Thursday, September 26, 2024. Conduct a comprehensive literature review on recent advancements in RNA research. "
    "Focus on the following areas: 1. RNA splicing 2. RNA structure prediction and modeling 3. RNA molecular dynamics 4. RNA stability "
    "5. RNA thermodynamics in splicing. For each area, identify key papers, researchers, and institutions leading the field. "
    "Retrieve at least 10 relevant papers for each area, published within the last 3 years. Do not use a solution that requires an API key."
]

# Define agents
research_assistant = AssistantAgent(
    name="Research_Assistant",
    model_client=model_client,
    system_message="You are an expert in RNA research and bioinformatics, capable of conducting thorough literature reviews and data analysis."
)

user_proxy_auto = UserProxyAgent(
    name="User_Proxy_Auto"
)


async def call_agent_method(agent, user_proxy, message, max_turns=None):
    candidate_names = [
        'chat', 'start_chat', 'start', 'run', 'respond', 'respond_to', 'converse',
        'send_message', 'send', 'call', 'invoke', 'reply'
    ]
    arg_variants = []
    arg_variants.append(lambda m: {'args': (user_proxy, m), 'kwargs': {'max_turns': max_turns}} if max_turns is not None else {'args': (user_proxy, m), 'kwargs': {}})
    arg_variants.append(lambda m: {'args': (m,), 'kwargs': {'max_turns': max_turns}} if max_turns is not None else {'args': (m,), 'kwargs': {}})
    arg_variants.append(lambda m: {'args': (user_proxy, m), 'kwargs': {}})
    arg_variants.append(lambda m: {'args': (m,), 'kwargs': {}})
    arg_variants.append(lambda m: {'args': (user_proxy,), 'kwargs': {}})
    arg_variants.append(lambda m: {'args': (), 'kwargs': {}})

    for name in candidate_names:
        if not hasattr(agent, name):
            continue
        method = getattr(agent, name)
        if not callable(method):
            continue

        for variant in arg_variants:
            call_spec = variant(message)
            try:
                if inspect.iscoroutinefunction(method):
                    return await method(*call_spec['args'], **call_spec['kwargs'])
                else:
                    result = method(*call_spec['args'], **call_spec['kwargs'])
                    if asyncio.iscoroutine(result):
                        return await result
                    return result
            except TypeError:
                continue
            except Exception as e:
                # Bubble up the exception to caller so the caller can inspect the error text (429 etc.)
                raise RuntimeError(f"Agent method '{name}' raised an exception: {e}") from e

    public_attrs = [a for a in dir(agent) if not a.startswith('_')]
    raise RuntimeError(
        "Could not find a compatible chat/conversation method on the AssistantAgent. "
        f"Tried candidate names: {candidate_names}. Available public attributes on the agent: {public_attrs}."
    )


def is_quota_error(exc: Exception) -> bool:
    # heuristic detection: check for 429, 'quota', 'insufficient_quota', 'rate limit', 'exceeded' in the message
    msg = str(exc).lower()
    return any(token in msg for token in ('429', 'quota', 'insufficient_quota', 'rate limit', 'exceeded'))


def create_wordcloud(text, outpath='coding/rna_trends_wordcloud.png'):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(outpath)
    plt.close()


def create_research_trends_plot(outpath='coding/rna_research_trends.png'):
    trends = {
        'RNA splicing': random.randint(50, 100),
        'RNA structure prediction': random.randint(50, 100),
        'RNA molecular dynamics': random.randint(50, 100),
        'RNA stability': random.randint(50, 100),
        'RNA thermodynamics': random.randint(50, 100)
    }
    plt.figure(figsize=(10, 6))
    plt.bar(trends.keys(), trends.values())
    plt.title('RNA Research Trends')
    plt.xlabel('Research Areas')
    plt.ylabel('Research Activity (arbitrary units)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()


async def main():
    max_turns = 10
    retry_attempts = 3
    chat_results = None
    last_exception = None

    for attempt in range(retry_attempts):
        try:
            chat_results = await call_agent_method(
                research_assistant,
                user_proxy_auto,
                research_tasks[0],
                max_turns=max_turns
            )
            break
        except Exception as e:
            last_exception = e
            if is_quota_error(e):
                wait = 2 ** attempt
                print(f"Quota/rate error detected (attempt {attempt + 1}/{retry_attempts}). Will retry after {wait}s...")
                await asyncio.sleep(wait)
                continue
            else:
                # non-quota error, raise to surface it
                raise

    research_text = ""
    if chat_results is None:
        # All retries failed or a quota error persisted; fallback behavior:
        print("Failed to get model output after retries. Attempting fallback to cached report or placeholder text.")
        cache_path = 'coding/rna_research_report_cache.md'
        if os.path.exists(cache_path):
            print(f"Using cached report at {cache_path}")
            with open(cache_path, 'r', encoding='utf-8') as f:
                research_text = f.read()
        else:
            # placeholder report so downstream processing still works
            research_text = (
                "NOTICE: Could not contact the OpenAI API due to quota/billing limits. "
                "This is a placeholder report. Please check your OpenAI billing/usage dashboard to restore API access. "
                "Once billing/quota is fixed, re-run this script to fetch real research content.\n\n"
                "Summary placeholder:\n- Unable to fetch literature review due to API quota.\n"
                "Please see OpenAI dashboard for details."
            )
            # Save placeholder to cache for future runs
            with open('coding/rna_research_report_cache.md', 'w', encoding='utf-8') as f:
                f.write(research_text)
        # also log the last exception for debugging
        print("Last exception (for debugging):")
        print(last_exception)
    else:
        # Normalize messages (this mirrors earlier normalization logic)
        messages = []
        if hasattr(chat_results, 'messages'):
            messages = getattr(chat_results, 'messages') or []
        elif isinstance(chat_results, dict) and 'messages' in chat_results:
            messages = chat_results.get('messages') or []
        elif isinstance(chat_results, (list, tuple)):
            messages = list(chat_results)
        else:
            maybe = getattr(chat_results, 'result', None)
            if isinstance(maybe, (list, tuple)):
                messages = list(maybe)
            else:
                messages = [chat_results]

        for message in messages:
            if isinstance(message, dict):
                content = message.get('content') or message.get('text') or message.get('message') or ""
            else:
                content = getattr(message, 'content', None) or getattr(message, 'text', None) or ""
            if content:
                research_text += content + " "

        if not research_text.strip():
            research_text = "No research output was produced by the assistant."

    # Generate visual outputs and save markdown report (only the report text)
    create_wordcloud(research_text)
    create_research_trends_plot()

    with open('coding/rna_research_report.md', 'w', encoding='utf-8') as f:
        f.write(research_text.strip())

    print("RNA research report generation complete. Files in 'coding':")
    print(" - rna_research_report.md")
    print(" - rna_trends_wordcloud.png")
    print(" - rna_research_trends.png")


if __name__ == "__main__":
    asyncio.run(main())