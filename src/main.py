import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
import os
from clean_aqi_data import *
from aqi_calculations import *
from borough_mapping import *

from io import BytesIO
import base64


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

    # Generate HTMLs for the annual AQI averages if they don't exist
    for year in ANNUAL_AQI_AVERAGE:
        map_filename = f"data/maps/Map_{year}.html"
        if not os.path.exists(map_filename):
            generate_annual_aqi_average_html(df, year, map_filename)
        else:
            print(f"{map_filename} exists")


    

    
    # TODO: ADD STREAMLIT TO RENDER HTML FROM DATA/MAPS DIRECTORY

    # st.title('NYC AQI Heatmap by Year')

    # # Slider for selecting year
    # year_index = st.slider('Select Year', min_value=0, max_value=len(ANNUAL_AQI_AVERAGE) - 1)

    # # Get selected year
    # selected_year = ANNUAL_AQI_AVERAGE[year_index]

    # # Load GeoJSON data
    # input_map = "data/nyc_community_districts.geojson"
    # gdf = gpd.read_file(input_map)

    # # Calculate AQI and color mapping for the selected year
    # color_and_aqi = {}
    # for boro in BORO_CDS:
    #     boro_cd = boro[0]
    #     districts = [boro[i] for i in range(1, len(boro))]
    #     average_aqi = calculate_aqi_average(df, selected_year, districts)
    #     color_and_aqi[boro_cd] = [interpolate_color(average_aqi), average_aqi]

    # # Add AQI value to GeoDataFrame properties
    # def add_aqi_to_properties(row):
    #     boro_cd = row['boro_cd']
    #     if boro_cd in color_and_aqi:
    #         row['aqi'] = color_and_aqi[boro_cd][1]
    #     else:
    #         row['aqi'] = 'N/A'
    #     return row

    # gdf = gdf.apply(add_aqi_to_properties, axis=1)

    # # Initialize the map
    # m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)

    # # Function to style features based on borough code
    # def style_function(feature):
    #     boro_cd = feature['properties'].get('boro_cd')
    #     color = color_and_aqi.get(boro_cd, ['gray', 'N/A'])
    #     return {
    #         'fillColor': color[0],
    #         'color': 'black',
    #         'weight': 1,
    #         'fillOpacity': 0.5
    #     }

    # # Add GeoJSON data to the map with custom styling
    # folium.GeoJson(
    #     gdf,
    #     style_function=style_function,
    #     highlight_function=lambda highlight: {'fillColor': 'blue'},
    #     overlay=True,
    #     tooltip=folium.GeoJsonTooltip(fields=['boro_cd', 'aqi'], aliases=['Borough Code:', 'AQI:'])
    # ).add_to(m)

    # # Save map to a BytesIO object and display in Streamlit
    # map_html = BytesIO()
    # m.save(map_html, close_file=False)
    # map_html.seek(0)

    # # Display the map in Streamlit
    # st.components.v1.html(map_html.getvalue().decode(), height=600)
    






















    




if __name__ == "__main__":
    main()