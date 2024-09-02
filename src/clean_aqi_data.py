import pandas as pd
from borough_mapping import *
from aqi_calculations import *
import geopandas as gpd
import folium
from branca.element import Template, MacroElement
import os

import matplotlib.pyplot as plt
import pickle
from sklearn.preprocessing import OneHotEncoder



def ensure_filtered_pollutants_csv(input_path, output_path, pollutants):   
    """
    Ensures and filters the dataset based on specific pollutants of interest 
    and saves the cleaned data to a CSV file.

    Parameters:
    - input_file  (str): Path to the input CSV file containing the raw AQI data.
    - output_file (str): Path where the cleaned CSV file will be saved.
    - pollutants  (list): list of pollutants to be filtered
    """       
    
    if not os.path.exists(output_path):
        df = pd.read_csv(input_path)
        cleaned_df = df[df["Name"].isin(pollutants)]
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


# Generate HTMLs for seasonal AQI averages if they don't exist
def ensure_seasonal_aqi_maps(df):
    for season in SEASONAL_AQI_AVERAGE:
        map_filename = f"data/maps/seasonal/Map_{season}.html"
        if not os.path.exists(map_filename):
            generate_aqi_average_html(df, season, map_filename, is_annual=False)
        else:
            print(f"{map_filename} exists")

## DONE
def ensure_annual_prediction_maps(years=5):
    curr_year = 2023
    for future_year in range(curr_year, curr_year + years):
        map_filename = f"data/maps/annual/Map_Annual Average Future {future_year}.html"
        if not os.path.exists(map_filename):
            generate_future_annual_aqi_average_html(future_year, map_filename, is_annual=True)
        else:
            print(f"{map_filename} exists")

## DONE
def generate_future_annual_aqi_average_html(future_year, map_filename, is_annual):
    
    print(f"Generating {map_filename}")

    with open('models/annual_model.pkl', 'rb') as file:
        model = pickle.load(file)
        
        # Mapping between boro_cd to a list containing: [color of aqi, predicted average aqi]
        color_and_aqi = {} 
        for boro in BORO_CDS:
            boro_cd = boro[0]     # Boro cd number
            pred_df = pd.DataFrame({'Borough CD': [boro_cd], 'Year': [future_year]})
            aqi_pred = model.predict(pred_df)
            aqi_extracted = aqi_pred[0, 0] # remove arrays from prediction
            color = interpolate_nyc_color(aqi_pred, is_annual)
            color_and_aqi[boro_cd] = [color, aqi_extracted]

    generate_html(color_and_aqi, map_filename)

# SEASONAL PREDICTIONS IP
################################################################################

##IP #########
def ensure_winter_prediction_maps(years=5):
    curr_year = 2023
    for future_year in range(curr_year, curr_year + years):    
        map_filename = f"data/maps/seasonal/Map_Winter_Future {future_year}.html"
        if not os.path.exists(map_filename):
            generate_future_seasonal_aqi_average_html(future_year, map_filename, is_annual=False)
        else:
            print(f"{map_filename} exists")

#IP FIX ME #########    
def generate_future_seasonal_aqi_average_html(winter_year, map_filename, is_annual):
    print(f"Generating {map_filename}")

    # Load the trained winter model
    with open('models/winter_model.pkl', 'rb') as file:
        model = pickle.load(file)

    # Define feature columns used for training
    feature_columns = ['Borough CD', 'Year']
    
    # Mapping between boro_cd to a list containing: [color of aqi, predicted average aqi]
    color_and_aqi = {} 
    for boro in BORO_CDS:
        boro_cd = boro[0]  # Boro cd number
        pred_df = pd.DataFrame({'Borough CD': [boro_cd], 'Year': [winter_year]})
        
        # Ensure all columns are in the same order as the training data
        for col in feature_columns:
            if col not in pred_df.columns:
                pred_df[col] = 0
        pred_df = pred_df[feature_columns]

        # Predict using the model
        aqi_pred = model.predict(pred_df)
        
        # Extract the predicted AQI value from the 1-dimensional array
        aqi_extracted = aqi_pred[0]  # remove arrays from prediction
        color = interpolate_nyc_color(aqi_extracted, is_annual)
        color_and_aqi[boro_cd] = [color, aqi_extracted]

    generate_html(color_and_aqi, map_filename)


################################################################################


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

    # Create a Macro Element object with the legend, and add it to the map as a child
    legend = MacroElement()
    legend._template = Template(legend_html)
    m.get_root().add_child(legend)

    m.save(map_filename)





## IP CLEAN
def ensure_annual_averages_csv(df, file_name):
    
    if not os.path.exists(file_name):
        # Initialize an empty list to store each row as a dictionary
        data = []

        # Iterate over each borough code and corresponding districts
        for boro in BORO_CDS:
            boro_cd = boro[0]     # Extract boro_cd number
            districts = boro[1:]  # Extract the list of districts

            # For each year in ANNUAL_AQI_AVERAGE, calculate the AQI and store the data
            for year in ANNUAL_AQI_AVERAGE:
                average_aqi = calculate_aqi_average(df, year, districts)  # Calculate AQI for the current year for the given districts
                
                # Append the data as a dictionary
                data.append({
                    'Borough CD': boro_cd,
                    'Year': year,
                    'Average AQI': average_aqi
                })
            
        # Convert the list of dictionaries into a DataFrame
        annual_df = pd.DataFrame(data)

        annual_df.to_csv(file_name, index=False)
        print(f"Annual Averages data has been saved in {file_name}")

def extract_second_year(s):
    return s.split(' ')[1].split('-')[1]


#IP CLEAN
def ensure_winter_averages_csv(df, file_name):
    
    if not os.path.exists(file_name):

        # Initialize an empty list to store each row as a dictionary
        data = []

        # Iterate over each borough code and corresponding districts
        for boro in BORO_CDS:
            boro_cd = boro[0]     # Extract boro_cd number
            districts = boro[1:]  # Extract the list of districts

            for winter in WINTER_AQI_AVERAGE:
                average_aqi = calculate_aqi_average(df, winter, districts)  # Calculate AQI for the current season for the given districts
                
                second_year = extract_second_year(winter)
                second_year = f'20{second_year}'
                # Append the data as a dictionary
                data.append({
                    'Borough CD': boro_cd,
                    'Year': second_year,
                    'Average AQI': average_aqi
                })
            
        # Convert the list of dictionaries into a DataFrame
        winter_df = pd.DataFrame(data)

        winter_df.to_csv(file_name, index=False)
        print(f"Winter Averages data has been saved in {file_name}")






# Checks if the annual scatter plots exist
def ensure_annual_grouped_scatter_plots(annual_df):
    for cd_num in range(100, 600, 100):
        scatter_path = f"assets/annual_scatter_plot_boro_cd_{cd_num}s.png"
        if not os.path.exists(scatter_path):
            generate_annual_scatter_plots(annual_df, cd_num, scatter_path)
        else:
            print(f"{scatter_path} exists")

# Generates annual scatter plots for each NYC borough
def generate_annual_scatter_plots(annual_df, cd_num, scatter_path):

    # Filter df based on borough cd range
    filtered_df = annual_df[(annual_df['Borough CD'] >= cd_num) & (annual_df['Borough CD'] < cd_num + 100)]

    plt.figure(figsize=(14, 8))
    
    # Create a scatter plot for the borough
    for boro_cd in filtered_df['Borough CD'].unique():
        subset = filtered_df[filtered_df['Borough CD'] == boro_cd]
        plt.scatter(subset['Year'], subset['Average AQI'], label=f'Borough CD {boro_cd}', s=50, alpha=0.7)
    
    plt.title(f'Scatter Plot of Average AQI Over Years for Borough CD {cd_num}s', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Average AQI', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Improve legend appearance
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Borough CD", fontsize=12, title_fontsize=14, ncol=2)
    
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Save the plot to a file
    plt.savefig(scatter_path, bbox_inches='tight')
    plt.close()  
    print(f"Scatter plot for Borough CD {cd_num}s has been saved in {scatter_path}")




