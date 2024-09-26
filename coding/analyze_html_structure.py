# filename: analyze_html_structure.py
html_content = """<PASTE_HTML_HERE>"""

def print_html_structure(html):
    # Print the relevant parts of the HTML for inspection
    start_section = html.find("<article class=")  # Starts of the article section
    end_section = html.find("</article>", start_section) + len("</article>")
    print(html[start_section:end_section])  # Print the first article section

print_html_structure(html_content)