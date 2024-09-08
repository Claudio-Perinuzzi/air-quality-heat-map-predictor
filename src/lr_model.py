from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pickle
import os

#############################################################################################
# Trains A Linear Regression Model for Predicting Future AQI Values
#############################################################################################

def ensure_lr_model(df, file_name):
    '''
    Ensures that a pickled linear regression model exists for the given file name.
    If the model does not exist, then the function trains a the model based on
    the given pre-filtered data frame consisting of either average annual, winter or summer
    AQI averages. The trained model is then pickled for subsequent use.
    '''

    if not os.path.exists(file_name):
        # Features and target
        features = ['Borough CD', 'Year']
        target = 'Average AQI'

        # Prepare the data
        X = df[features]
        y = df[target]

        # align y with X
        y = y[X.index]  

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

