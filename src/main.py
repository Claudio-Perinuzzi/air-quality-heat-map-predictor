import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import os
from clean_aqi_data import *
from aqi_calculations import *
from borough_mapping import *

# TODO:
# Implement a option for a button to change the color for a more drastic appearence, 
# the highest mean in the data set will be the end color
# This will be more apparent for the predictive model
    # possibly use a choropleth map where different ranges of aqi are rep with diff colors
    # may help in distinguishing beteween various ranges more clearly


def main():
    
    # Raw/clean data paths and polutants of interest
    input_path  = "data/raw_aqi_data.csv"
    output_path = "data/cleaned_aqi_data.csv"
    polutants   = ["Fine particles (PM 2.5)", "Nitrogen dioxide (NO2)", "Ozone (O3)"]

    # Filter the polutants of interest if the cleaned data set is not present
    if not os.path.exists(output_path):
        filter_polutants(input_path, output_path, polutants)

    # Generate a data frame and append the AQI caluclations to each row
    df = pd.read_csv(output_path)
    append_aqi_to_df(df)

    #TODO Put in respective tabs & refactor ######################################

    # Generate HTMLs for the annual AQI averages if they don't exist
    for year in ANNUAL_AQI_AVERAGE:
        map_filename = f"data/maps/annual/Map_{year}.html"
        if not os.path.exists(map_filename):
            generate_annual_aqi_average_html(df, year, map_filename)
        else:
            print(f"{map_filename} exists")


    # Generate HTMLs for seasonal AQI averages if they don't exisit
    for season in SEASONAL_AQI_AVERAGE:
        map_filename = f"data/maps/seasonal/Map_{season}.html"
        if not os.path.exists(map_filename):
            generate_seasonal_aqi_average_html(df, season, map_filename)
        else:
            print(f"{map_filename} exists")


    # TODO: Refactor Tabs
    # Render HTML to Streamlit ########################################
    # Create Tabs
    tab1, tab2 = st.tabs(["Annual AQI Average", "Seasonal AQI Averwge"])

    # Annual AQI Average tab
    with tab1:
        st.title("NYC Annual Average AQI Heatmap")

        # Render slidebar and map slidebar value index to annual aqi average tuple
        year_index = st.slider("Select Year", min_value=2009, max_value=2022)
        selected_year = ANNUAL_AQI_AVERAGE[year_index - 2009]

        # Display the title of the given map
        st.markdown(f"""
            <h1 style="text-align: center; font-size: 28px;">
                AQI {selected_year}
            </h1>
        """, unsafe_allow_html=True)

        # Generate map name based on user's choice and render the HTML to streamlit
        map_name = f"data/maps/annual/Map_{selected_year}.html"
        with open(map_name, "r") as file:
            html_content = file.read()
        st.components.v1.html(html_content, height=600)
    
    with tab2:
        st.title("NYC Seasonal Average AQI Heatmap")

        # Render slidebar and map slidebar value index to seasonal aqi average tuple
        season_index = st.slider("Select Season", min_value=0, max_value=len(SEASONAL_AQI_AVERAGE) - 1)
        selected_season = SEASONAL_AQI_AVERAGE[season_index]

        # Display the title of the given map
        st.markdown(f"""
            <h1 style="text-align: center; font-size: 28px;">
                AQI {selected_season}
            </h1>
        """, unsafe_allow_html=True)

        # Generate map name based on user's choice and render the HTML to streamlit
        map_name = f"data/maps/seasonal/Map_{selected_season}.html"
        with open(map_name, "r") as file:
            html_content = file.read()
        st.components.v1.html(html_content, height=600)

    
 

    

    






















    




if __name__ == "__main__":
    main()