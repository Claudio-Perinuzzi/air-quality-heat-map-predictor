import matplotlib.pyplot as plt
from aqi_constants import *
import os

#############################################################################################
# Scatter Plot Functions
#
# Functions include:
#   - Ensuring plots exist in the asset directory
#   - Generating plots given the annual, winter or summer aqi average data frame
#############################################################################################


def ensure_grouped_scatter_plots(df, time):
    '''
    Checks if the scatter plots exist in the asset directory
    If not, generates the scatter plot for the given borrough
    '''
    
    for cd_num in range(100, 600, 100):
        if time == 'Annual':
            scatter_path = f"assets/annual_scatter_plot_boro_cd_{cd_num}s.png"
        elif time == 'Winter':
            scatter_path = f"assets/winter_scatter_plot_boro_cd_{cd_num}s.png"
        elif time == 'Summer':
            scatter_path = f"assets/summer_scatter_plot_boro_cd_{cd_num}s.png"
        else:
            raise ValueError(f"Invalid time frame: {time}. Expected 'Annual', 'Winter', or 'Summer'.")
        
        if not os.path.exists(scatter_path):
            generate_scatter_plots(df, cd_num, scatter_path, time)
        else:
            print(f"{scatter_path} exists")


def generate_scatter_plots(df, cd_num, scatter_path, time):
    '''
    Generates scatter plots for each NYC borugh given the season
    '''

    # Get the borough name from the cd number
    boro = CD_TO_BORO[cd_num]

    # Filter df based on borough cd range
    boro_cd_condition = (df['Borough CD'] >= cd_num) & (df['Borough CD'] < cd_num + 100)
    boro_df = df[boro_cd_condition]

    plt.figure(figsize=(14, 8))
    
    # Create a scatter plot for the borough
    for boro_cd in boro_df['Borough CD'].unique():
        matching_boro_condition = boro_df['Borough CD'] == boro_cd
        subset = boro_df[matching_boro_condition]
        plt.scatter(subset['Year'], subset['Average AQI'], label=f'Borough CD {boro_cd}', s=50, alpha=0.7)
    
    plt.title(f'Scatter Plot of {time} AQI Averages Over The Years {boro}', fontsize=16)
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

