import pandas as pd


def clean_aqi_data(input_path, output_path):
    """
    Filters the AQI dataset based on specific pollutants of interest 
    and saves the cleaned data to a CSV file.

    Parameters:
    - input_file  (str): Path to the input CSV file containing the raw AQI data.
    - output_file (str): Path where the cleaned CSV file will be saved.

    The function filters rows where the 'Name' column matches specific pollutants, 
    and saves the filtered DataFrame to the specified output file.
    """
    
    df = pd.read_csv(input_path)

    # Pollutants of interest
    names_to_be_filtered = ["Fine particles (PM 2.5)",
                            "Nitrogen dioxide (NO2)", 
                            "Ozone (O3)"]

    cleaned_df = df[df["Name"].isin(names_to_be_filtered)]

    cleaned_df.to_csv(output_path, index=False)
    print(f"Filtered data has been saved in {output_path}")


