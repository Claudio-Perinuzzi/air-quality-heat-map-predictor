from aqi_data_cleaning import *
from aqi_scatter_plots import *
from aqi_calculations import *
from aqi_constants import *
from aqi_html_maps import *
from lr_model import *
import streamlit as st


def initialize():
    '''
    Initializes the system by checking and cleaning the raw dataset, calculating AQI values,
    calculating and filtering average AQI values for each borough and training a linear regression
    model to predict future AQI values given the past data.
    '''

    if 'initialized' not in st.session_state: # Initialize only once
        st.session_state['initialized'] = True
        print("Initializing...")

        #############################################################################################
        # Clean/filter raw data, append AQI calculations and ensure past annual & seasonal maps exist
        #############################################################################################

        # Filter the pollutants of interest if the cleaned data set is not present
        ensure_filtered_pollutants_csv(
            input_path  = "data/raw_aqi_data.csv",
            output_path = "data/cleaned_aqi_data.csv",
            pollutants  = ["Fine particles (PM 2.5)", "Nitrogen dioxide (NO2)", "Ozone (O3)"]
        )

        # Generate a data frame with columns of interest
        df = pd.read_csv(
            filepath_or_buffer = "data/cleaned_aqi_data.csv",        
            usecols = ["Name", "Geo Place Name", "Time Period", "Data Value"]
        )
        
        # Append the AQI calculations to each row of the data frame
        append_aqi_to_df(df)

        # Generate HTMLs for the past annual and seasonal AQI averages if they don't exist
        ensure_annual_aqi_maps(df)
        ensure_seasonal_aqi_maps(df)


        ############################################################################################# 
        # Annual Predictions
        #############################################################################################

        # Generate a CSV dataset with annual averages for each borough cd if it does not exist
        annual_input_path = "data/annual_aqi_averages.csv"
        ensure_averages_csv(df, annual_input_path, time='Annual Averages')

        # Read the data into a dataframe and convert 'Year' column to numerical values
        annual_df = pd.read_csv(annual_input_path)
        
        # Creates a scatter plot of AQI averages for each district over the years
        ensure_grouped_scatter_plots(annual_df, time='Annual')

        # Train a linear regression model if a pickle of the model does not exist
        ensure_lr_model(annual_df, file_name='models/annual_model.pkl')

        # Generate future year AQI predictions maps if they do not exist
        ensure_prediction_maps(time='Annual', years=5) # 5 years in advance by default


        #############################################################################################
        # Winter Predictions 
        #############################################################################################

        winter_input_path = "data/winter_aqi_averages.csv"
        ensure_averages_csv(df, winter_input_path, time='Winter')

        winter_df = pd.read_csv(winter_input_path)

        # Creates a scatter plot of AQI averages for each district over the years
        ensure_grouped_scatter_plots(winter_df, time='Winter')

        # Train a linear regression model if a pickle of the model does not exist
        ensure_lr_model(winter_df, file_name='models/winter_model.pkl')

        # Generate future year AQI predictions maps if they do not exist
        ensure_prediction_maps(time="Winter", years=5) # 5 years in advance 


        #############################################################################################
        # Summer Predictions 
        #############################################################################################

        summer_input_path = "data/summer_aqi_averages.csv"
        ensure_averages_csv(df, summer_input_path, time='Summer')

        summer_df = pd.read_csv(summer_input_path)

        # Creates a scatter plot of AQI averages for each district over the years
        ensure_grouped_scatter_plots(summer_df, time='Summer')

        # Train a linear regression model if a pickle of the model does not exist
        ensure_lr_model(summer_df, file_name='models/summer_model.pkl')

        # Generate future year AQI predictions maps if they do not exist
        ensure_prediction_maps(time="Summer", years=5) # 5 years in advance 