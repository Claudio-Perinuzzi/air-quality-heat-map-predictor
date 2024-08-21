import streamlit as st
import os
import pandas as pd
from clean_aqi_data import *
from calculate_aqi import *

import geopandas as gpd
import folium


def main():
    
    # input_path  = "data/raw_aqi_data.csv"
    # output_path = "data/cleaned_aqi_data.csv"

    # if not os.path.exists(output_path):
    #     clean_aqi_data(input_path, output_path)

    # df = pd.read_csv(output_path)

    # # Calculate the AQI for each pollutant
    # df.loc[df["Name"] == "Fine particles (PM 2.5)", "AQI"] = df["Data Value"].apply(calculate_aqi_pm25)
    # df.loc[df["Name"] == "Nitrogen dioxide (NO2)", "AQI"] = df["Data Value"].apply(calculate_aqi_no2)
    # df.loc[df["Name"] == "Ozone (O3)", "AQI"] = df["Data Value"].apply(calculate_aqi_o3)


    # Testing maps
    input_map = "data/nyc_community_districts.geojson"
    gdf = gpd.read_file(input_map)
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    folium.GeoJson(gdf).add_to(m)

    m.save("Map.html")








if __name__ == "__main__":
    main()