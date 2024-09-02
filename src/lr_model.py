from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
# from sklearn.preprocessing import OneHotEncoder
from borough_mapping import *
import pandas as pd
import pickle
import os

# CLEAN UP



def ensure_winter_lr_model(winter_df, file_name='models/winter_model.pkl'):
    if not os.path.exists(file_name):
        # Features and target
        features = ['Borough CD', 'Year']
        target = 'Average AQI'

        # Prepare the data
        X = winter_df[features]
        y = winter_df[target]

        # Ensure 'Year' is treated as integer
        X['Year'] = X['Year'].astype(int)

        # Check if 'Borough CD' is numeric
        if not pd.api.types.is_numeric_dtype(X['Borough CD']):
            X['Borough CD'] = pd.to_numeric(X['Borough CD'], errors='coerce')
        
        # Drop rows with NaN values if any
        X.dropna(inplace=True)
        y = y[X.index]  # align y with X

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Linear Regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # List of predicted AQI values for the test set
        y_pred = model.predict(X_test)
        print("Predicted AQI values:", y_pred)

        # Evaluate the model by comparing the test set and prediction set
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

        # Save the model
        with open(file_name, 'wb') as file:
            pickle.dump(model, file)
            print(f"Linear regression model created and saved in {file_name}")


def ensure_annual_lr_model(annual_df, file_name='models/annual_model.pkl'):
    if not os.path.exists(file_name):

        # Features and target variable
        features = ['Borough CD', 'Year']
        target = ['Average AQI']
        X = annual_df[features]
        y = annual_df[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        #list of predicted AQI values for the test set
        y_pred = model.predict(X_test)
        #print(y_pred)

        # Evaluate the model, compare b/w test set and prediction set
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')

        # # Example of predicting future AQI value
        # new_data = pd.DataFrame({'Borough CD': [101], 'Year': [2023]})
        # future_aqi_pred = model.predict(new_data)
        # print(f'Predicted AQI value for future data: {future_aqi_pred[0]}')

        # new_data = pd.DataFrame({'Borough CD': [101], 'Year': [2024]})
        # future_aqi_pred = model.predict(new_data)
        # print(f'Predicted AQI value for future data: {future_aqi_pred[0]}')

        # new_data = pd.DataFrame({'Borough CD': [101], 'Year': [2025]})
        # future_aqi_pred = model.predict(new_data)
        # print(f'Predicted AQI value for future data: {future_aqi_pred[0]}')

        # new_data = pd.DataFrame({'Borough CD': [503], 'Year': [2028]})
        # future_aqi_pred = model.predict(new_data)
        # print(f'Predicted AQI value for future data: {future_aqi_pred[0]}')

        #saves the file
        with open('models/annual_model.pkl', 'wb') as file:
            pickle.dump(model, file)
            print(f"Linear regression model created and saved in {file_name}")

        #1 to 5 years

# 101,Annual Average 2009,24.85
# 101,Annual Average 2010,22.75
# 101,Annual Average 2011,22.9
# 101,Annual Average 2012,21.2
# 101,Annual Average 2013,20.7
# 101,Annual Average 2014,20.15
# 101,Annual Average 2015,18.65
# 101,Annual Average 2016,17.95
# 101,Annual Average 2017,17.45
# 101,Annual Average 2018,17.15
# 101,Annual Average 2019,16.35
# 101,Annual Average 2020,14.6
# 101,Annual Average 2021,14.65
# 101,Annual Average 2022,14.1