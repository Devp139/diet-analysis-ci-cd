#importing the libraries needed
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading dataset
df = pd.read_csv("All_Diets.csv")

# Handling missing values by filling with column mean
df[['Protein(g)', 'Carbs(g)', 'Fat(g)']] = df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].fillna(
    df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
)

# Calculating average macronutrients per diet type
avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
print("\nAverage Macronutrients per Diet Type:\n")
print(avg_macros)

# Calculating top 5 protein-rich recipes per diet
top_protein = df.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
top_protein.to_csv("top_5_protein_recipes.csv", index=False)

# Calculating diet with highest protein content
highest_protein_diet = avg_macros['Protein(g)'].idxmax()
print("\nDiet with highest average protein:", highest_protein_diet)

# Calculating most common cuisine per diet type
common_cuisine = df.groupby('Diet_type')['Cuisine_type'].agg(lambda x: x.value_counts().idxmax())
print("\nMost common cuisine per diet type:\n")
print(common_cuisine)


# New Metrics
df['Protein_to_Carbs_ratio'] = df['Protein(g)'] / df['Carbs(g)']
df['Carbs_to_Fat_ratio'] = df['Carbs(g)'] / df['Fat(g)']

df.to_csv("processed_diet_data.csv", index=False)

# Visualizations
# Bar Chart of the Average Protein by Diet Type
plt.figure(figsize=(10, 5))
sns.barplot(x=avg_macros.index, y=avg_macros['Protein(g)'])
plt.title("Average Protein by Diet Type")
plt.ylabel("Protein (g)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("avg_protein_by_diet.png")
plt.show()

# Heatmap of Macronutrients 
plt.figure(figsize=(8, 6))
sns.heatmap(avg_macros, annot=True, fmt=".1f",cmap="YlGnBu")
plt.title("Macronutrient Heatmap by Diet Type")
plt.ylabel("Diet Type")
plt.tight_layout()
plt.savefig("macronutrient_heatmap.png")  
plt.show()  


# Scatter Plot of the Top Protein Recipes
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=top_protein,
    x='Protein(g)',
    y='Carbs(g)',
    hue='Cuisine_type'
)
plt.title("Top 5 Protein-Rich Recipes by Cuisine")
plt.tight_layout()
plt.savefig("top_protein_scatter.png")
plt.show()

print("\nCalculation completed. Files and charts saved in the folder.")
