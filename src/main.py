from aqi_initialize import * 
from aqi_constants import *
import streamlit as st

#############################################################################################
# Main Function 
#   - Initializes the system once which:
#       - Checks, cleans and filters the AQI dataset
#       - Calculates the average AQI
#       - Generates HTML Maps and scatter plots
#       - Trains linear regression models
#   - Handles the rest of the streamlit UI logic
#############################################################################################

#TODO: TOOL tip, shows if future? finalize requirements, 
# make a portfolio? YES! ADD MY JAVA PROJ THERE TOO!!! HAVE TO FIX IT, can i run in streamlit?
# yes you have to call a jar file pretty much

def main(): 
    
    # Initlaize the system once and check to make sure all assets are available
    initialize()

    # Define Tabs
    annual_tab, seasonal_tab = st.tabs(["Annual AQI Average", "Seasonal AQI Average"])

    # Annual AQI Average tab
    with annual_tab:
        annual_tab()
    
    # Seasonal AQI Average tab
    with seasonal_tab:
        seasonal_tab()


# Annual AQI Average tab
def annual_tab():
    st.title("NYC Annual Average AQI Heatmap")

    # Render slidebar and map slidebar value index to annual aqi average tuple
    year_index = st.slider("Select Year", min_value=2009, max_value=2027)
    selected_year = ANNUAL_SCROLL_BAR[year_index - 2009]

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
def seasonal_tab():
    st.title("NYC Seasonal Average AQI Heatmap")

    # Render slide bar and map slide bar value index to seasonal aqi average tuple
    season_index = st.slider("Select Season", min_value=0, max_value=len(SEASONAL_SCROLL_BAR) - 1)
    selected_season = SEASONAL_SCROLL_BAR[season_index]

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