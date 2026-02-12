import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from azure.storage.blob import BlobServiceClient
import io
import json

# Function to process data from Azurite (local Azure Blob Storage emulator)
def process_nutritional_data_from_azurite():
    # Connect to Azurite Blob Storage (local Azure storage emulator)
    connect_str = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;" \
                  "AccountKey=Eby8vdM02xNOcqFeqCnrC4xF..." \
                  "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"

    # Initialize the Blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    container_name = 'datasets'
    blob_name = 'All_Diets.csv'

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    # Download the CSV file as bytes
    stream = blob_client.download_blob().readall()
    df = pd.read_csv(io.BytesIO(stream))

    # Process data and calculate insights
    avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

    # Save processed results
    result = avg_macros.reset_index().to_dict(orient='records')

    with open('simulated_nosql/results.json', 'w') as f:
        json.dump(result, f)

    print("\nAverage Macronutrients per Diet Type:\n")
    print(avg_macros)

    # Save the result as CSV
    df.to_csv("processed_diet_data.csv", index=False)

    return avg_macros  # Returning the result

# Main data analysis and visualization code
def analyze_data():
    # Loading dataset (if processing locally, use this)
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
    sns.heatmap(avg_macros, annot=True, fmt=".1f", cmap="YlGnBu")
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

# Run the analysis function if executed directly
if __name__ == "__main__":
    analyze_data()


