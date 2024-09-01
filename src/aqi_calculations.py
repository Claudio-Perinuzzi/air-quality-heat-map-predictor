import pandas as pd
from borough_mapping import *


# Appends the calculated AQI for each pollutant in the dataframe
def append_aqi_to_df(df):
    df.loc[df["Name"] == "Fine particles (PM 2.5)", "AQI"] = df["Data Value"].apply(calculate_aqi_pm25)
    df.loc[df["Name"] == "Nitrogen dioxide (NO2)", "AQI"] = df["Data Value"].apply(calculate_aqi_no2)
    df.loc[df["Name"] == "Ozone (O3)", "AQI"] = df["Data Value"].apply(calculate_aqi_o3)


# Helper function for calculating the AQI for the given concentration and its defined breakpoints
def calculate_aqi(concentration, breakpoints):
    for bp_low, bp_high, i_low, i_high in breakpoints:
        if bp_low <= concentration <= bp_high:
            aqi = ((i_high - i_low) / (bp_high - bp_low)) * (concentration - bp_low) + i_low
            return int(round(aqi))

    return None


# Calculate particulate matter of 2.5 micrometers in diameter (PM2.5)
def calculate_aqi_pm25(concentration):

    # As per EPA guidelines, truncate to 1 decimal place
    concentration = float(f"{concentration:.1f}")

    pm25_breakpoints = [
        (0.0, 9.0, 0, 50),
        (9.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 125.4, 151, 200),
        (125.5, 225.4, 201, 300),
        (225.5, float('inf'), 301, float('inf'))
    ]
    
    return calculate_aqi(concentration, pm25_breakpoints)


# Calculate nitrogen dioxide (NO2)
def calculate_aqi_no2(concentration):
    
    # As per EPA guidelines, truncate to integer
    concentration = int(concentration)

    no2_breakpoints = [
        (0, 53, 0, 50),
        (54, 100, 51, 100),
        (101, 360, 101, 150),
        (361, 649, 151, 200),
        (650, 1249, 201, 300),
        (1250, float('inf'), 301, float('inf'))    
    ]

    return calculate_aqi(concentration, no2_breakpoints)


# Calculate ozone (O3), measured an average of 8 hours in NYC
def calculate_aqi_o3(concentration):
    
    # As per EPA guidelines, truncate to 3 decimal places
    concentration = float(f"{concentration:.3f}")

    o3_breakpoints = [
        (0, 54, 0, 50),
        (55, 70, 51, 100),
        (71, 85, 101, 150),
        (86, 105, 151, 200),
        (106, 200, 201, 300),
        (201, float('inf'), 301, float('inf'))    
    ]

    return calculate_aqi(concentration, o3_breakpoints)


def calculate_aqi_average(df, time_period, districts): 
    '''
    Function that calculates the average AQI for a given boro_cd during a certain time_period

    df          -> data frame
    time_period -> str, time period pollutant was calculated during
    districts   -> list, list of districts for the given boro_cd
    '''

    # Running collection of all aqi vals
    all_aqi_vals = [] 

    # For every district, filter the data frame based on location and time period
    # Collect AQI values from the filtered data frame and extend to all AQI values list
    for district in districts:
        filtered_df = df[(df['Geo Place Name'] == district) & (df['Time Period'] == time_period)]
        aqi_vals = filtered_df['Data Value']
        all_aqi_vals.extend(aqi_vals)
   
    # Convert to Pandas Series, convert to numeric and drop NaNs
    all_aqi_vals = pd.Series(all_aqi_vals).apply(pd.to_numeric, errors='coerce').dropna()
    
    # Calculate and return the average
    if len(all_aqi_vals) > 0:
        average_value = all_aqi_vals.mean()
    else:
        average_value = None  
    
    return float(f"{average_value:.2f}")



def interpolate_true_color(aqi):
    '''
    Function that interpolates the true standardized AQI colors as defined below.
    NYC's 5 boroughs are relatively in the good and moderate range so the heatmap
    won't tell use much how AQI changes over the years/seasons, the interpolate_nyc_color 
    function below is used instead specifically for nyc to visual how AQI changes over the years/seasons

    Source: https://docs.airnowapi.org/aq101
    AQI Numbers	    AQI Category (Descriptor)	AQI Color	  Hexadecimal Color Value	Category Number
    0 - 50	        Good	                    Green	        (00e400)	            1
    51 - 100	    Moderate	                Yellow	        (ffff00)	            2
    101 - 150	    Unhealthy Sensitive Group	Orange	        (ff7e00)	            3
    151 - 200	    Unhealthy	                Red	            (ff0000)	            4
    201 - 300	    Very Unhealthy	            Purple	        (8f3f97)	            5
    301 - 500	    Hazardous	                Maroon	        (7e0023)	            6
    '''

    # If a negative value is passed in, set the AQI to 0
    aqi = max(aqi, 0)
    
    # AQI breakpoints to corresponding RGB values
    aqi_colors = [
        (0,   (0, 228, 0)),     # Green
        (50,  (255, 255, 0)),   # Yellow
        (100, (255, 126, 0)),   # Orange
        (150, (255, 0, 0)),     # Red
        (200, (143, 63, 151)),  # Purple
        (300, (126, 0, 35))     # Maroon
    ]

    # Find the lower and upper RGB colors for the passed in AQI
    for i in range(len(aqi_colors) - 1):
        if aqi_colors[i][0] <= aqi <= aqi_colors[i + 1][0]:
            lower_aqi, lower_color = aqi_colors[i]
            upper_aqi, upper_color = aqi_colors[i + 1]
            break
    else:
        # AQI is over range, then return the upper color
        upper_color = aqi_colors[-1][1]
        return f'#{upper_color[0]:02x}{upper_color[1]:02x}{upper_color[2]:02x}'


    # Calculate the ratio of the AQI within this range
    ratio = (aqi - lower_aqi) / (upper_aqi - lower_aqi)

    # Interpolate the RGB values from the upper and lower RGB color bounds and return this RGB color
    r = int(lower_color[0] + (upper_color[0] - lower_color[0]) * ratio)
    g = int(lower_color[1] + (upper_color[1] - lower_color[1]) * ratio)
    b = int(lower_color[2] + (upper_color[2] - lower_color[2]) * ratio)
    
    return f'#{r:02x}{g:02x}{b:02x}'




def interpolate_nyc_color(aqi, is_annual):
    '''
    Custom interpolating color function for NYC's borough average max and min values
    Note:   NYC averages good to low moderate air quality. By defining a custom interpolating color,
            with color endpoints ranging from the lowest to highest average AQI, we can visualize
            NYC's heatmap better. The AQI colors defined here are not standardized and are used for
            visual purposes.
    '''

    # Respective min and max average AQI values for the given season
    if is_annual:
        min_aqi = NYC_ANNUAL_MIN_AQI     # AQI = 7.38
        max_aqi = NYC_ANNUAL_MAX_AQI     # AQI = 27.45
    else:
        min_aqi = NYC_SEASONAL_MIN_AQI   # AQI = 10.1 
        max_aqi = NYC_SEASONAL_MAX_AQI   # AQI = 30.83

    # Step size used to create evenly spaced intervals
    step = (max_aqi - min_aqi) / 5

    # Define the color stops
    aqi_colors = [
        (min_aqi, (0, 228, 0)),                 # Green
        (min_aqi + step, (255, 255, 0)),        # Yellow
        (min_aqi + 2 * step, (255, 126, 0)),    # Orange
        (min_aqi + 3 * step, (255, 0, 0)),      # Red
        (min_aqi + 4 * step, (143, 63, 151)),   # Purple
        (max_aqi, (126, 0, 35))                 # Maroon
    ]

    # Find the lower and upper RGB colors for the passed in AQI
    for i in range(len(aqi_colors) - 1):
        if aqi_colors[i][0] <= aqi <= aqi_colors[i + 1][0]:
            lower_aqi, lower_color = aqi_colors[i]
            upper_aqi, upper_color = aqi_colors[i + 1]
            break
    else:
        # AQI is over range, then return the upper color
        upper_color = aqi_colors[-1][1]
        return f'#{upper_color[0]:02x}{upper_color[1]:02x}{upper_color[2]:02x}'


    # Calculate the ratio of the AQI within this range
    ratio = (aqi - lower_aqi) / (upper_aqi - lower_aqi)

    # Interpolate the RGB values from the upper and lower RGB color bounds and return this RGB color
    r = int(lower_color[0] + (upper_color[0] - lower_color[0]) * ratio)
    g = int(lower_color[1] + (upper_color[1] - lower_color[1]) * ratio)
    b = int(lower_color[2] + (upper_color[2] - lower_color[2]) * ratio)
    
    return f'#{r:02x}{g:02x}{b:02x}'
