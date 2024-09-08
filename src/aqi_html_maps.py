from branca.element import Template, MacroElement
from aqi_calculations import *
from aqi_constants import *
import geopandas as gpd
import pandas as pd
import folium
import pickle
import os

#############################################################################################
# AQI HTML Generation Functions
#
# Functions that include:
#   - Ensuring past and future annual and seasonal HTML maps exist
#   - Generation of HTML maps for past and future annual and seasonal AQI averages
#############################################################################################


def ensure_annual_aqi_maps(df):
    '''
    Ensures annual AQI maps exist. If they do not exist, 
    then the function will call generate_aqi_average_html
    '''

    for year in ANNUAL_AQI_AVERAGE:
        map_filename = f"data/maps/annual/Map_{year}.html"
        if not os.path.exists(map_filename):
            generate_aqi_average_html(df, year, map_filename, is_annual=True)
        else:
            print(f"{map_filename} exists")


def ensure_seasonal_aqi_maps(df):
    '''
    Ensures seasonal AQI maps exist. If they do not exist, 
    then the function will call generate_aqi_average_html
    '''
    
    for season in SEASONAL_AQI_AVERAGE:
        map_filename = f"data/maps/seasonal/Map_{season}.html"
        if not os.path.exists(map_filename):
            generate_aqi_average_html(df, season, map_filename, is_annual=False)
        else:
            print(f"{map_filename} exists")


def ensure_prediction_maps(time, years=5):
    '''
    Ensures predicted future AQI maps exist. If they do not exist, 
    then the function will call generate_future_aqi_average_html    
    '''

    curr_year = 2023
    for future_year in range(curr_year, curr_year + years):

        if time == 'Annual':
            map_filename = f"data/maps/annual/Map_Annual Average {future_year} (Future).html"
            model_path = 'models/annual_model.pkl'
        elif time == 'Winter':
            map_filename = f"data/maps/seasonal/Map_Winter {future_year} (Future).html"
            model_path = 'models/winter_model.pkl'
        elif time == 'Summer':
            map_filename = f"data/maps/seasonal/Map_Summer {future_year} (Future).html"
            model_path = 'models/summer_model.pkl'        
        else:
            raise ValueError(f"Invalid time frame: {time}. Expected 'Annual', 'Winter', or 'Summer'.")

        if not os.path.exists(map_filename):
            generate_future_aqi_average_html(future_year, map_filename, model_path, time)
        else:
            print(f"{map_filename} exists")


def generate_future_aqi_average_html(future_year, map_filename, model_path, time):
    '''
    Generates predicted future AQI average HTMLs
    '''
    
    print(f"Generating {map_filename}")

    with open(model_path, 'rb') as file:
        model = pickle.load(file)
        
        is_annual = True if time == 'Annual' else False

        # Mapping between boro_cd to a list containing: [color of aqi, predicted average aqi]
        color_and_aqi = {} 
        for boro in BORO_CDS:
            boro_cd = boro[0]     # Boro cd number
            pred_df = pd.DataFrame({'Borough CD': [boro_cd], 'Year': [future_year]})
            aqi_pred = model.predict(pred_df)
            aqi_extracted = aqi_pred[0]
            color = interpolate_nyc_color(aqi_pred, is_annual)
            color_and_aqi[boro_cd] = [color, aqi_extracted]

    generate_html(color_and_aqi, map_filename)


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

    generate_html(color_and_aqi, map_filename)


def generate_html(color_and_aqi, map_filename):
    '''
    Generates & saves HTMLs of a NYC GeoJSON with appended average AQI calculations
    '''

    # Load GeoJSON data
    input_map = "data/nyc_community_districts.geojson"
    gdf = gpd.read_file(input_map)
    
    # Add AQI value to GeoDataFrame properties
    def add_aqi_to_properties(row):
        boro_cd = row['boro_cd']
        if boro_cd in color_and_aqi:
            # Add in aqi value to the GeoDataFrame
            aqi_val_extracted = color_and_aqi[boro_cd][1]
            aqi_val_rounded = round(aqi_val_extracted, 2)
            row['aqi'] = aqi_val_rounded  # Add AQI value

            # Add in the borough to the GeoDataFrame
            cd_num_rounded = (int(boro_cd) // 100) * 100
            row['borough'] = CD_TO_BORO[cd_num_rounded]
        else:
            row['aqi'] = 'N/A'
            row['borough'] = 'N/A'
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
        tooltip=folium.GeoJsonTooltip(fields=['borough', 'boro_cd', 'aqi'], aliases=['Borough', 'District Code:', 'AQI:'])
    ).add_to(m)

    # Define legend HTML style
    legend_html = NYC_LEGEND_HTML # See borough_mapping.py for custom HTML

    # Create a Macro Element object with the legend, and add it to the map as a child
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    m.save(map_filename)


