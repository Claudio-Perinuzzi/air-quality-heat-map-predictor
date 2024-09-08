from aqi_calculations import *
from aqi_constants import *
import pandas as pd
import os

#############################################################################################
# CSV Dataset Cleaning Functions
#
# Functions that include:
#   - Filtering pollutants of interest are filtered and saved in a clean CSV.
#   - Filtering annual, winter and summer AQI averages into seperate CSVs which are
#     subsequently used to train a linear regression model.
#############################################################################################

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


def get_annual_aqi_averages(data, df, boro_cd, districts):  
    '''
    Returns an appended list of the annual aqi averages for the 
    given districts (helper function to ensure_averages_csv)
    '''

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


def get_winter_aqi_averages(data, df, boro_cd, districts):
    '''
    Returns an appended list of the winter aqi averages for the 
    given districts (helper function to ensure_averages_csv)
    '''

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


def get_summer_aqi_averages(data, df, boro_cd, districts):
    '''
    Returns an appended list of the summer aqi averages for the 
    given districts (helper function to ensure_averages_csv)
    '''

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


def ensure_averages_csv(df, file_name, time):
    '''
    Ensures that the annual, winter and summer AQI average CSVs exist.
    If they do not exist, then the function will generate them 
    by calling get_{time}_aqi_averages given the time frame
    '''

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

        add_aqi_differences(df)


        df.to_csv(file_name, index=False)
        print(f"{time} data has been saved in {file_name}")


def add_aqi_differences(df):
    gb =  df.groupby('Borough CD')
    df['aqi_diff_prev_year'] = gb['Average AQI'].diff()
    df['aqi_diff_prev_year'] = df['aqi_diff_prev_year'].fillna(0).round(2)
