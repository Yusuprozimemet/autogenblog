# filename: retrieve_rna_research_news.py
import requests

# List of RNA research full names
rna_research_full_names = [
    "Functional viromic screens uncover regulatory RNA elements.",
    "Chloroplast gene expression: Recent advances and perspectives.",
    "RNA-based translation activators for targeted gene upregulation."
]

def fetch_news(headline):
    search_url = f"https://www.bing.com/news/search?q={headline.replace(' ', '%20')}"
    response = requests.get(search_url)

    if response.status_code != 200:
        print(f"Failed to retrieve news for '{headline}'. Status code: {response.status_code}")
        return []

    headlines = []
    # Attempt to pull out headlines from the HTML response
    start_index = 0
    while len(headlines) < 10:
        title_index = response.text.find(' class="title"', start_index)
        if title_index == -1:
            break

        title_start = response.text.find('>', title_index) + 1
        title_end = response.text.find('</a>', title_start)
        headline_text = response.text[title_start:title_end].strip()

        headlines.append(headline_text)
        start_index = title_end

    return headlines

# Collect news headlines
all_headlines = {}
for name in rna_research_full_names:
    all_headlines[name] = fetch_news(name)

# Print headlines
for full_name, headlines in all_headlines.items():
    print(f"Headlines for '{full_name}':")
    for headline in headlines:
        print(f"- {headline}")
    print()  # Add an empty line for better readability