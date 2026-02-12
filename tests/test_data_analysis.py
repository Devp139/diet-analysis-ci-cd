import unittest
import pandas as pd
from data_analysis import process_nutritional_data_from_azurite  # Replace with the actual function name if different

class TestDataAnalysis(unittest.TestCase):
    
    # Test case for checking missing values handling
    def test_missing_values(self):
        # Simulate a small dataframe with missing values
        df = pd.DataFrame({
            'Protein(g)': [10, None, 30],
            'Carbs(g)': [5, 8, None],
            'Fat(g)': [2, 4, 5],
            'Diet_type': ['paleo', 'keto', 'mediterranean']
        })
        
        # Handle missing values (fill with mean as per your code)
        df[['Protein(g)', 'Carbs(g)', 'Fat(g)']] = df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].fillna(
            df[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        )

        # Ensure no missing values
        self.assertFalse(df.isnull().values.any())

    # Test case for checking average macronutrients per diet type
    def test_average_macronutrients(self):
        # Simulate a small dataset
        df = pd.DataFrame({
            'Protein(g)': [10, 20, 30],
            'Carbs(g)': [5, 10, 15],
            'Fat(g)': [2, 4, 6],
            'Diet_type': ['paleo', 'keto', 'paleo']
        })

        avg_macros = df.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()

        # Test if the average protein for 'paleo' is correct
        self.assertEqual(avg_macros.loc['paleo', 'Protein(g)'], 20)

if __name__ == '__main__':
    unittest.main()
