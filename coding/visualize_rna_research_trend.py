# filename: visualize_rna_research_trend.py
import matplotlib.pyplot as plt

years = [2023, 2024]
number_of_papers = [3, 1]  # Example count based on static data

plt.figure(figsize=(10, 6))
plt.bar(years, number_of_papers, color='royalblue')
plt.title('RNA Research Trends Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.xticks(years)
plt.grid(axis='y')

# Save the figure to a file
plt.savefig('research_trend.png')
plt.show()

print("Visualization saved as research_trend.png.")