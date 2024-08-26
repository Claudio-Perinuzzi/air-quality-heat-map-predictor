import pandas as pd
from borough_mapping import *
from aqi_calculations import *
import geopandas as gpd
import folium
from branca.element import Template, MacroElement



def filter_polutants(input_path, output_path, polutants):
    """
    Filters the AQI dataset based on specific pollutants of interest 
    and saves the cleaned data to a CSV file.

    Parameters:
    - input_file  (str): Path to the input CSV file containing the raw AQI data.
    - output_file (str): Path where the cleaned CSV file will be saved.
    - polutants   (list): list of pollutants to be filtered

    The function filters rows where the 'Name' column matches specific pollutants, 
    and saves the filtered DataFrame to the specified output file.
    """
    
    df = pd.read_csv(input_path)

    cleaned_df = df[df["Name"].isin(polutants)]

    cleaned_df.to_csv(output_path, index=False)
    print(f"Filtered data has been saved in {output_path}")


# Generates htmls of annual aqi averages
def generate_annual_aqi_average_html(df, year, map_filename):  
    print(f"Generating {map_filename}")

    # Mapping between boro_cd to color of aqi and average aqi
    color_and_aqi = {}
    for boro in BORO_CDS:
        boro_cd = boro[0]  # e.g., "101"
        districts = [boro[i] for i in range(1, len(boro))]  # List of districts
        average_aqi = calculate_aqi_average(df, year, districts)  # Calculate AQI for current year
        color_and_aqi[boro_cd] = [interpolate_color(average_aqi), average_aqi]
    
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
    legend_html = '''
    {% macro html(this, kwargs) %}

    <div style="
        position: fixed; 
        bottom: 20px; 
        left: 50%; 
        transform: translateX(-50%);
        width: 90%;  /* Increase width */
        height: 60px;  /* Increase height */
        background: linear-gradient(to right, rgb(0, 228, 0), rgb(255, 255, 0), rgb(255, 126, 0), rgb(255, 0, 0), rgb(143, 63, 151), rgb(126, 0, 35)); 
        border:2px solid black; 
        z-index:1000; 
        font-size:12px;
        line-height: 1.2em;  /* Adjust line height */
        color: black;  /* Set font color to black */
        text-align: center;
        padding: 5px 10px;  /* Add padding */
        box-sizing: border-box;
    ">

        <span style="float:left; width: 12%; text-align: center;"><strong>0-50</strong><br>(Good)</span>
        <span style="float:left; width: 12%; text-align: center;"><strong>51-100</strong><br>(Moderate)</span>
        <span style="float:left; width: 18%; text-align: center;"><strong>101-150</strong><br>(Unhealthy for Sensitive Groups)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>151-200</strong><br>(Unhealthy)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>201-300</strong><br>(Very Unhealthy)</span>
        <span style="float:right; width: 14%; text-align: center;"><strong>301-500</strong><br>(Hazardous)</span>
    </div>

    {% endmacro %}
    '''

    # Crate a Macro Element object with the legend, and add it to the map as a child
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    # Save the map to an HTML file with year in filename
    map_filename = f"data/maps/annual/Map_{year}.html"
    m.save(map_filename)



#TODO: REFACTOR ABOVE & BOTTOM FUNCTIONS, SAME CODE
def generate_seasonal_aqi_average_html(df, year, map_filename):
    print(f"Generating {map_filename}")

    # Mapping between boro_cd to color of aqi and average aqi
    color_and_aqi = {}
    for boro in BORO_CDS:
        boro_cd = boro[0]  # e.g., "101"
        districts = [boro[i] for i in range(1, len(boro))]  # List of districts
        average_aqi = calculate_aqi_average(df, year, districts)  # Calculate AQI for current year
        color_and_aqi[boro_cd] = [interpolate_color(average_aqi), average_aqi]
    
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
    legend_html = '''
    {% macro html(this, kwargs) %}

    <div style="
        position: fixed; 
        bottom: 20px; 
        left: 50%; 
        transform: translateX(-50%);
        width: 90%;  /* Increase width */
        height: 60px;  /* Increase height */
        background: linear-gradient(to right, rgb(0, 228, 0), rgb(255, 255, 0), rgb(255, 126, 0), rgb(255, 0, 0), rgb(143, 63, 151), rgb(126, 0, 35)); 
        border:2px solid black; 
        z-index:1000; 
        font-size:12px;
        line-height: 1.2em;  /* Adjust line height */
        color: black;  /* Set font color to black */
        text-align: center;
        padding: 5px 10px;  /* Add padding */
        box-sizing: border-box;
    ">

        <span style="float:left; width: 12%; text-align: center;"><strong>0-50</strong><br>(Good)</span>
        <span style="float:left; width: 12%; text-align: center;"><strong>51-100</strong><br>(Moderate)</span>
        <span style="float:left; width: 18%; text-align: center;"><strong>101-150</strong><br>(Unhealthy for Sensitive Groups)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>151-200</strong><br>(Unhealthy)</span>
        <span style="float:left; width: 14%; text-align: center;"><strong>201-300</strong><br>(Very Unhealthy)</span>
        <span style="float:right; width: 14%; text-align: center;"><strong>301-500</strong><br>(Hazardous)</span>
    </div>

    {% endmacro %}
    '''

    # Crate a Macro Element object with the legend, and add it to the map as a child
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    # Save the map to an HTML file with year in filename
    map_filename = f"data/maps/seasonal/Map_{year}.html"
    m.save(map_filename)