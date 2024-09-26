# filename: static_rna_research_data.py
research_data = [
    {
        "title": "Functional viromic screens uncover regulatory RNA elements.",
        "authors": "Seo JJ, Jung SJ, Yang J, Choi DE, Kim VN.",
        "journal": "Cell. 2023.",
        "pmid": "37413987",
    },
    {
        "title": "Chloroplast gene expression: Recent advances and perspectives.",
        "authors": "Zhang Y, Tian L, Lu C.",
        "journal": "Plant Commun. 2023.",
        "pmid": "37147800",
    },
    {
        "title": "RNA-based translation activators for targeted gene upregulation.",
        "authors": "Cao Y, Liu H, Lu SS, Jones KA, Govind AP, Jeyifous O, Simmons CQ, Tabatabaei N, Green WN, Holder JL Jr, Tahmasebi S, George AL Jr, Dickinson BC.",
        "journal": "Nat Commun. 2023.",
        "pmid": "37884512",
    },
    # Add more research papers as necessary
]

# Save this data to a structured file
with open("rna_research_data.txt", "w") as file:
    for research in research_data:
        file.write(f"Title: {research['title']}\n")
        file.write(f"Authors: {research['authors']}\n")
        file.write(f"Journal: {research['journal']}\n")
        file.write(f"PMID: {research['pmid']}\n\n")

print("RNA research data has been saved.")