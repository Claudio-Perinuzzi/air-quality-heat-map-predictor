import pandas as pd
from borough_mapping import *
from aqi_calculations import *
import geopandas as gpd
import folium
from branca.element import Template, MacroElement
import os
import matplotlib.pyplot as plt
import pickle



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


# returns an appended list of the annual aqi averages for the given districts (helper function to ensure_averages_csv)
def get_annual_aqi_averages(data, df, boro_cd, districts):  
    # For each year in ANNUAL_AQI_AVERAGE, calculate the AQI and store the data
    for year in ANNUAL_AQI_AVERAGE:
        average_aqi = calculate_aqi_average(df, year, districts)  # Calculate AQI for the current year for the given districts
        year_date = year.split(' ')[2]
        # Append the data as a dictionary
        data.append({
            'Borough CD': boro_cd,
            'Year': year_date,
            'Average AQI': average_aqi
        })
    return data

# returns an appended list of the winter aqi averages for the given districts (helper function to ensure_averages_csv)
def get_winter_aqi_averages(data, df, boro_cd, districts):
    # For each winter, calculate the AQI and store the data
    for winter in WINTER_SEASONS:
        average_aqi = calculate_aqi_average(df, winter, districts)  # Calculate AQI for the current winter for the given districts
        second_year = winter.split(' ')[1].split('-')[1] # Splits the string on spqces, gets the second element and does it again on - to get the second year
        second_year = f'20{second_year}'
        # Append the data as a dictionary
        data.append({
            'Borough CD': boro_cd,
            'Year': second_year,
            'Average AQI': average_aqi
        })
    return data

# returns an appended list of the summer aqi averages for the given districts (helper function to ensure_averages_csv)
def get_summer_aqi_averages(data, df, boro_cd, districts):
    # For each summer, calculate the AQI and store the data
    for summer in SUMMER_SEASONS:
        average_aqi = calculate_aqi_average(df, summer, districts)  # Calculate AQI for the current summer for the given districts
        summer_year = summer.split()[1]  # Split the string by spaces and get the second element which represents the year
        # Append the data as a dictionary
        data.append({
            'Borough CD': boro_cd,
            'Year': summer_year,
            'Average AQI': average_aqi
        })
    return data


# ensures that the annual, winter and summer AQI average CSVs exist and if not, generates them
def ensure_averages_csv(df, file_name, time):
    if not os.path.exists(file_name):

        # Initialize an empty list to store each row as a dictionary
        data = []   

        for boro in BORO_CDS:       # Iterate over each borough code and corresponding districts
            boro_cd = boro[0]       # Extract boro_cd number
            districts = boro[1:]    # Extract the list of districts

            # get the correct aqi averages for the given time frame for the given boro_cds and append it to the data list
            if time == 'Annual Averages':
                get_annual_aqi_averages(data, df, boro_cd, districts)
            elif time == 'Winter':
                get_winter_aqi_averages(data, df, boro_cd, districts)
            elif time == 'Summer':
                get_summer_aqi_averages(data, df, boro_cd, districts)
            else:
                raise ValueError(f"Invalid time frame: {time}. Expected 'Annual Averages', 'Winter', or 'Summer'.")
            
        # Convert the list of dictionaries into a DataFrame and save it
        df = pd.DataFrame(data)
        df.to_csv(file_name, index=False)
        print(f"{time} data has been saved in {file_name}")


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


# Ensure that the future prediciton maps exits, if not, generate them
def ensure_prediction_maps(time, years=5):
    curr_year = 2023
    for future_year in range(curr_year, curr_year + years):

        if time == 'Annual':
            map_filename = f"data/maps/annual/Map_Annual Average Future {future_year}.html"
            model_path = 'models/annual_model.pkl'
        elif time == 'Winter':
            map_filename = f"data/maps/seasonal/Map_Winter_Future {future_year}.html"
            model_path = 'models/winter_model.pkl'
        elif time == 'Summer':
            map_filename = f"data/maps/seasonal/Map_Summer_Future {future_year}.html"
            model_path = 'models/summer_model.pkl'        
        else:
            raise ValueError(f"Invalid time frame: {time}. Expected 'Annual', 'Winter', or 'Summer'.")

        if not os.path.exists(map_filename):
            generate_future_aqi_average_html(future_year, map_filename, model_path, time)
        else:
            print(f"{map_filename} exists")


# Generate future AQI average HTMLs
def generate_future_aqi_average_html(future_year, map_filename, model_path, time):
    
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







##### REVIEW SCATTER PLOTS


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




