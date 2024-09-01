# nyc-air-quality-heat-map-predictor

## Usage

Application for displaying past and predicted future values of the air quality index (AQI) over New York City's five borough district communities. 

## Introduction

Air pollution poses significant risks to both the environment and public health. In the summer of 2023, New York City's skyline turned orange due to smoke from Canadian wildfires, highlighting the importance of monitoring air quality. Although this dataset only extends through 2022, it provides valuable insights into the city's air quality trends.

On average, New York City's AQI remains below 50, placing it in the "Good" category. However, certain high-traffic areas, such as Midtown, often experience elevated PM2.5 levels compared to surrounding regions, which can lead to localized pollution concerns. To visualize the contrast between boroughs more effectively, a custom RGB color interpolation function was applied with the low and high bounds of the colors reflecting the respective lowest and highest average AQI values in the dataset.

The average AQI was calculated for each of the boroughs' air pollutants for the given seasons/years. The pollutants analyzed include:

- Fine particles (PM 2.5)
- Nitrogen dioxide (NO2)
- Ozone (O3)

The AQI calculations performed in this application follow the May 2024 EPA Air Quality Reporting Document: [View the PDF](resources/EPA/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf)

## Dataset Used

This dataset contains the name of the airborne pollutant, time and place of measurement, as well as the average value of the measurement. 

Dataset source: [NYC Open Data AQI](https://data.cityofnewyork.us/Environment/Air-Quality/c3uy-2p5r/about_data)

## Example User Interface

NYC's annual average air quality index for the year 2009. The distribution of AQI values highlights regions with varied air quality, indicating both better and worse air quality zones.

![Alt Text](assets/1_annual_average_2009.jpg)

NYC's annual average air quality index for the year 2022. The averages here reflect changes in the air quality over the years as compared to 2009. 

![Alt Text](assets/2_annual_average_2022.jpg)

Close up showing the AQI for given the borough code.

![Alt Text](assets/3_close_up_annual_average_2009.jpg)

## Next Steps

Predictive model to display future values in progress.