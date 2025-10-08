import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np

def create_additional_datetime_features(df):
    """
    Add additional datetime-related features to the DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing at least the columns 'datetime_s' and 'datetime_e', 
        which represent the start and end datetimes, respectively.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with additional columns:
        - 'is_holiday': Boolean column indicating if 'datetime_s' falls on a Dutch national holiday.
        - 'weekday': Integer column representing the day of the week for 'datetime_s'.
        - 'hour': Integer column representing the hour of the day for 'datetime_s'.
        - 'duration': Timedelta column representing the difference between 'datetime_e' and 'datetime_s'.
        - 'duration_in_s': Integer column representing the duration in seconds.
    """
    holidays_nl = [
        # 2018
        ["2018-01-01", "New Year's Day"],
        ["2018-03-30", "Good Friday"],
        ["2018-04-01", "Easter Sunday"],
        ["2018-04-02", "Easter Monday"],
        ["2018-04-27", "King's Birthday"],
        ["2018-05-04", "National Remembrance Day"],
        ["2018-05-05", "Liberation Day"],
        ["2018-05-10", "Ascension Day"],
        ["2018-05-20", "Whit Sunday"],
        ["2018-05-21", "Whit Monday"],
        ["2018-12-25", "Christmas Day"],
        ["2018-12-26", "St. Stephen's Day"],
    
        # 2019
        ["2019-01-01", "New Year's Day"],
        ["2019-04-19", "Good Friday"],
        ["2019-04-21", "Easter Sunday"],
        ["2019-04-22", "Easter Monday"],
        ["2019-04-27", "King's Birthday"],
        ["2019-05-04", "National Remembrance Day"],
        ["2019-05-05", "Liberation Day"],
        ["2019-05-30", "Ascension Day"],
        ["2019-06-09", "Whit Sunday"],
        ["2019-06-10", "Whit Monday"],
        ["2019-12-25", "Christmas Day"],
        ["2019-12-26", "St. Stephen's Day"],
    
        # 2020
        ["2020-01-01", "New Year's Day"],
        ["2020-04-10", "Good Friday"],
        ["2020-04-12", "Easter Sunday"],
        ["2020-04-13", "Easter Monday"],
        ["2020-04-27", "King's Birthday"],
        ["2020-05-04", "National Remembrance Day"],
        ["2020-05-05", "Liberation Day"],
        ["2020-05-21", "Ascension Day"],
        ["2020-05-31", "Whit Sunday"],
        ["2020-06-01", "Whit Monday"],
        ["2020-12-25", "Christmas Day"],
        ["2020-12-26", "St. Stephen's Day"],
    
        # 2021
        ["2021-01-01", "New Year's Day"],
        ["2021-04-02", "Good Friday"],
        ["2021-04-04", "Easter Sunday"],
        ["2021-04-05", "Easter Monday"],
        ["2021-04-27", "King's Birthday"],
        ["2021-05-04", "National Remembrance Day"],
        ["2021-05-05", "Liberation Day"],
        ["2021-05-13", "Ascension Day"],
        ["2021-05-23", "Whit Sunday"],
        ["2021-05-24", "Whit Monday"],
        ["2021-12-25", "Christmas Day"],
        ["2021-12-26", "St. Stephen's Day"],
    
        # 2022
        ["2022-01-01", "New Year's Day"],
        ["2022-04-15", "Good Friday"],
        ["2022-04-17", "Easter Sunday"],
        ["2022-04-18", "Easter Monday"],
        ["2022-04-27", "King's Birthday"],
        ["2022-05-04", "National Remembrance Day"],
        ["2022-05-05", "Liberation Day"],
        ["2022-05-26", "Ascension Day"],
        ["2022-06-05", "Whit Sunday"],
        ["2022-06-06", "Whit Monday"],
        ["2022-12-25", "Christmas Day"],
        ["2022-12-26", "St. Stephen's Day"],
    
        # 2023
        ["2023-01-01", "New Year's Day"],
        ["2023-04-07", "Good Friday"],
        ["2023-04-09", "Easter Sunday"],
        ["2023-04-10", "Easter Monday"],
        ["2023-04-27", "King's Birthday"],
        ["2023-05-04", "National Remembrance Day"],
        ["2023-05-05", "Liberation Day"],
        ["2023-05-18", "Ascension Day"],
        ["2023-05-28", "Whit Sunday"],
        ["2023-05-29", "Whit Monday"],
        ["2023-12-25", "Christmas Day"],
        ["2023-12-26", "St. Stephen's Day"],
    
        # 2024
        ["2024-01-01", "New Year's Day"],
        ["2024-03-29", "Good Friday"],
        ["2024-03-31", "Easter Sunday"],
        ["2024-04-01", "Easter Monday"],
        ["2024-04-27", "King's Birthday"],
        ["2024-05-04", "National Remembrance Day"],
        ["2024-05-05", "Liberation Day"],
        ["2024-05-09", "Ascension Day"],
        ["2024-05-19", "Whit Sunday"],
        ["2024-05-20", "Whit Monday"],
        ["2024-12-25", "Christmas Day"],
        ["2024-12-26", "St. Stephen's Day"]
    ]

    df['is_holiday'] = df["datetime_s"].dt.date.isin([pd.to_datetime(holiday[0]).date() for holiday in holidays_nl])
    df['weekday'] = df['datetime_s'].dt.dayofweek
    df['hour'] = df['datetime_s'].dt.hour
    
    return df

def load_and_predict(model_path, input_data):
    """
    Load a Keras .h5 model and make a prediction on input data.
    
    Parameters:
    - model_path (str): Path to the .h5 model file.
    - input_data (numpy array): Input data for making predictions.
    
    Returns:
    - prediction: Model prediction for the input data.
    """
    # Load the model
    model = load_model(model_path)
    
    # Make a prediction
    prediction = model.predict(input_data)
    
    return prediction

def combine_functions(temp, rain, streetname, gforce, speedlimit, windspeed, datetime):
    """
    Combine the data preparation and prediction functions.

    Parameters:
    -----------
    temp : float
        Temperature.
    rain : float
        Rainfall.
    streetname : str
        Street name (assuming this is categorical data).
    gforce : float
        G-force.
    speedlimit : int
        Speed limit.
    windspeed : float
        Wind speed.
    datetime : str
        Datetime in ISO format (e.g., '2024-06-19T12:00:00').

    Returns:
    --------
    float
        Model prediction result.
    """
    # Construct the DataFrame with input data
    df = pd.DataFrame({
        'temp': [temp],
        'rain': [rain],
        'streetname': [streetname],
        'gforce': [gforce],
        'speedlimit': [speedlimit],
        'windspeed': [windspeed],
        'datetime_s': pd.to_datetime(datetime),
        'datetime_e': pd.to_datetime(datetime)
    })

    # Add datetime features
    df = create_additional_datetime_features(df)
    encoder = LabelEncoder()
    encoder.classes_ = np.load('weights_files/classes_streetname.npy')
    df['streetname'] = encoder.transform(df['streetname']

    # Extract input features for prediction
    input_data = df[['streetname', 'temp', 'rain', 'gforce', 'speedlimit', 'windspeed', 'is_holiday', 'weekday', 'hour', 'duration_in_s']].values

    # Load and predict using the model
    model_path = 'path_to_model.h5'  # Replace with actual path
    prediction = load_and_predict(model_path, input_data)

    return prediction[0]
