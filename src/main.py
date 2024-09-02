import streamlit as st
import pandas as pd
from clean_aqi_data import *
from aqi_calculations import *
from borough_mapping import *
from lr_model import *



# TODO: predictive model


def main(): 
    
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

########################### Annual

    # Generate a CSV dataset with annual averages for each borough cd if it does not exist
    annual_input_path = "data/annual_aqi_averages.csv"
    ensure_annual_averages_csv(df, annual_input_path)

    # Read the data into a dataframe and convert 'Year' column to numerical values
    annual_df = pd.read_csv(annual_input_path)
    annual_df['Year'] = annual_df['Year'].str.extract(r'(\d+)').astype(int)    
    
    # Creates a scatter plot of AQI averages for each district over the years
    ensure_annual_grouped_scatter_plots(annual_df)

    # Train a linear regression model if a pickle of the model does not exist
    ensure_annual_lr_model(annual_df)

    # Generate future year AQI predictions maps if they do not exist
    ensure_annual_prediction_maps(years=5) # 5 years in advance by default

############################# Seasonal

    winter_input_path = "data/winter_aqi_averages.csv"
    ensure_winter_averages_csv(df, winter_input_path)

    winter_df = pd.read_csv(winter_input_path)

    # Train a linear regression model if a pickle of the model does not exist
    ensure_winter_lr_model(winter_df)

    # # Generate future year AQI predictions maps if they do not exist
    ensure_winter_prediction_maps() # 5 years in advance 



    # # Generate HTMLs for the annual and seasonal AQI averages if they don't exist
    # ensure_annual_aqi_maps(df)
    # ensure_seasonal_aqi_maps(df)


    # # Define Tabs
    # tab1, tab2 = st.tabs(["Annual AQI Average", "Seasonal AQI Average"])

    # # Annual AQI Average tab
    # with tab1:
    #     tab_1()
    
    # # Seasonal AQI Average tab
    # with tab2:
    #     tab_2()

    
 



# Annual AQI Average tab
def tab_1():
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


# Seasonal AQI Average tab
def tab_2():
    st.title("NYC Seasonal Average AQI Heatmap")

    # Render slide bar and map slide bar value index to seasonal aqi average tuple
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