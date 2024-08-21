import unittest
import pandas as pd
from src.clean_aqi_data import clean_aqi_data
import os

# python -m unittest discover -s tests

class TestCleanAQIData(unittest.TestCase):
    
    # Prepares the test fixture
    def setUp(self):
        self.input_file = 'data/raw_aqi_data.csv'
        self.output_file = 'data/test_cleaned_aqi_data.csv'

    def test_clean_aqi_data(self):

        # Read in raw data and test data
        raw_df = pd.read_csv(self.input_file)
        clean_aqi_data(self.input_file, self.output_file)
        test_df = pd.read_csv(self.output_file)
        
        # Count the names for each data frame
        raw_count_of_names = {
            "pm25": (raw_df["Name"] == "Fine particles (PM 2.5)").sum(),
            "nO2":  (raw_df["Name"] == "Nitrogen dioxide (NO2)").sum(),
            "O3":   (raw_df["Name"] == "Ozone (O3)").sum()
        }

        test_count_of_names = {
            "pm25": (test_df["Name"] == "Fine particles (PM 2.5)").sum(),
            "nO2":  (test_df["Name"] == "Nitrogen dioxide (NO2)").sum(),
            "O3":   (test_df["Name"] == "Ozone (O3)").sum()
        }

        # Assert counts are the same
        self.assertEqual(raw_count_of_names["pm25"], test_count_of_names["pm25"])
        self.assertEqual(raw_count_of_names["nO2"],  test_count_of_names["nO2"])
        self.assertEqual(raw_count_of_names["O3"],   test_count_of_names["O3"])

   
    # Clean up files after testing
    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)


if __name__ == "__main__":
    unittest.main()