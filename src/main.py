import os
import pandas as pd
from clean_aqi_data import *
from calculate_aqi import *




def main():
    
    input_path  = "data/raw/raw_aqi_data.csv"
    output_path = "data/cleaned/cleaned_aqi_data.csv"

    if not os.path.exists(output_path):
        clean_aqi_data(input_path, output_path)

    df = pd.read_csv(output_path)

    # Calculate the AQI for each pollutant
    df.loc[df["Name"] == "Fine particles (PM 2.5)", "AQI"] = df["Data Value"].apply(calculate_aqi_pm25)
    df.loc[df["Name"] == "Nitrogen dioxide (NO2)", "AQI"] = df["Data Value"].apply(calculate_aqi_no2)
    df.loc[df["Name"] == "Ozone (O3)", "AQI"] = df["Data Value"].apply(calculate_aqi_o3)









if __name__ == "__main__":
    main()