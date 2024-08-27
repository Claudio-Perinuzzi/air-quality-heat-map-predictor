import pandas as pd
from borough_mapping import *
from aqi_calculations import *
import geopandas as gpd
import folium
from branca.element import Template, MacroElement
import os


def ensure_filtered_polutants_cvs(input_path, output_path, polutants):   
    """
    Ensures and filters the dataset based on specific pollutants of interest 
    and saves the cleaned data to a CSV file.

    Parameters:
    - input_file  (str): Path to the input CSV file containing the raw AQI data.
    - output_file (str): Path where the cleaned CSV file will be saved.
    - polutants   (list): list of pollutants to be filtered
    """       
    
    if not os.path.exists(output_path):
        df = pd.read_csv(input_path)
        cleaned_df = df[df["Name"].isin(polutants)]
        cleaned_df.to_csv(output_path, index=False)
        print(f"Filtered data has been saved in {output_path}")



# Generate HTMLs for the annual AQI averages if they don't exist
def ensure_annual_aqi_maps(df):
    for year in ANNUAL_AQI_AVERAGE:
        map_filename = f"data/maps/annual/Map_{year}.html"
        if not os.path.exists(map_filename):
            generate_aqi_average_html(df, year, map_filename, is_annual=True)
        else:
            print(f"{map_filename} exists")


# Generate HTMLs for seasonal AQI averages if they don't exisit
def ensure_seasonal_aqi_maps(df):
    for season in SEASONAL_AQI_AVERAGE:
        map_filename = f"data/maps/seasonal/Map_{season}.html"
        if not os.path.exists(map_filename):
            generate_aqi_average_html(df, season, map_filename, is_annual=False)
        else:
            print(f"{map_filename} exists")


def generate_aqi_average_html(df, year, map_filename, is_annual):  
    '''
    Generates HTML Maps of annual or seasonal AQI district averages. 
    These averages get mapped to the GeoJSON defined boundaries.
    '''

    print(f"Generating {map_filename}")

    # Mapping between boro_cd to a list containing: [color of aqi, average aqi]
    color_and_aqi = {} 
    for boro in BORO_CDS:
        boro_cd = boro[0]     # Boro cd number
        districts = boro[1:]  # List of districts
        average_aqi = calculate_aqi_average(df, year, districts)  # Calculate AQI for current year for the given list of districts
        color_and_aqi[boro_cd] = [interpolate_nyc_color(average_aqi, is_annual), average_aqi]

    # Load GeoJSON data
    input_map = "data/nyc_community_districts.geojson"
    gdf = gpd.read_file(input_map)
    
    # Add AQI value to GeoDataFrame properties
    def add_aqi_to_properties(row):
        boro_cd = row['boro_cd']
        if boro_cd in color_and_aqi:
            row['aqi'] = color_and_aqi[boro_cd][1]  # Add AQI value to 'aqi' property
        else:
            row['aqi'] = 'N/A'
        return row

    gdf = gdf.apply(add_aqi_to_properties, axis=1)

    # Initialize the map
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=10)
    
    # Function to style features based on borough code
    def style_function(feature):
        boro_cd = feature['properties'].get('boro_cd')
        color = color_and_aqi.get(boro_cd, ['gray', 'N/A'])
        return {
            'fillColor': color[0],
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.5
        }
    
    # Add GeoJSON data to the map with custom styling
    folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=lambda highlight: {'fillColor': 'blue'},
        overlay=True,
        tooltip=folium.GeoJsonTooltip(fields=['boro_cd', 'aqi'], aliases=['Borough Code:', 'AQI:'])
    ).add_to(m)

    # Define legend HTML style
    legend_html = NYC_LEGEND_HTML # See borough_mapping.py for custom HTML

    # Crate a Macro Element object with the legend, and add it to the map as a child
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    # Save the map to an HTML file with year or season in filename
    if is_annual:
        map_filename = f"data/maps/annual/Map_{year}.html"
    else:
        map_filename = f"data/maps/seasonal/Map_{year}.html"

    m.save(map_filename)
