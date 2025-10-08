from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os

# Define functions here
def create_additional_datetime_features(df):
    holidays_nl = [
        ["2018-01-01", "New Year's Day"], ["2018-03-30", "Good Friday"], ["2018-04-01", "Easter Sunday"],
        ["2018-04-02", "Easter Monday"], ["2018-04-27", "King's Birthday"], ["2018-05-04", "National Remembrance Day"],
        ["2018-05-05", "Liberation Day"], ["2018-05-10", "Ascension Day"], ["2018-05-20", "Whit Sunday"],
        ["2018-05-21", "Whit Monday"], ["2018-12-25", "Christmas Day"], ["2018-12-26", "St. Stephen's Day"],
        ["2019-01-01", "New Year's Day"], ["2019-04-19", "Good Friday"], ["2019-04-21", "Easter Sunday"],
        ["2019-04-22", "Easter Monday"], ["2019-04-27", "King's Birthday"], ["2019-05-04", "National Remembrance Day"],
        ["2019-05-05", "Liberation Day"], ["2019-05-30", "Ascension Day"], ["2019-06-09", "Whit Sunday"],
        ["2019-06-10", "Whit Monday"], ["2019-12-25", "Christmas Day"], ["2019-12-26", "St. Stephen's Day"],
        ["2020-01-01", "New Year's Day"], ["2020-04-10", "Good Friday"], ["2020-04-12", "Easter Sunday"],
        ["2020-04-13", "Easter Monday"], ["2020-04-27", "King's Birthday"], ["2020-05-04", "National Remembrance Day"],
        ["2020-05-05", "Liberation Day"], ["2020-05-21", "Ascension Day"], ["2020-05-31", "Whit Sunday"],
        ["2020-06-01", "Whit Monday"], ["2020-12-25", "Christmas Day"], ["2020-12-26", "St. Stephen's Day"],
        ["2021-01-01", "New Year's Day"], ["2021-04-02", "Good Friday"], ["2021-04-04", "Easter Sunday"],
        ["2021-04-05", "Easter Monday"], ["2021-04-27", "King's Birthday"], ["2021-05-04", "National Remembrance Day"],
        ["2021-05-05", "Liberation Day"], ["2021-05-13", "Ascension Day"], ["2021-05-23", "Whit Sunday"],
        ["2021-05-24", "Whit Monday"], ["2021-12-25", "Christmas Day"], ["2021-12-26", "St. Stephen's Day"],
        ["2022-01-01", "New Year's Day"], ["2022-04-15", "Good Friday"], ["2022-04-17", "Easter Sunday"],
        ["2022-04-18", "Easter Monday"], ["2022-04-27", "King's Birthday"], ["2022-05-04", "National Remembrance Day"],
        ["2022-05-05", "Liberation Day"], ["2022-05-26", "Ascension Day"], ["2022-06-05", "Whit Sunday"],
        ["2022-06-06", "Whit Monday"], ["2022-12-25", "Christmas Day"], ["2022-12-26", "St. Stephen's Day"],
        ["2023-01-01", "New Year's Day"], ["2023-04-07", "Good Friday"], ["2023-04-09", "Easter Sunday"],
        ["2023-04-10", "Easter Monday"], ["2023-04-27", "King's Birthday"], ["2023-05-04", "National Remembrance Day"],
        ["2023-05-05", "Liberation Day"], ["2023-05-18", "Ascension Day"], ["2023-05-28", "Whit Sunday"],
        ["2023-05-29", "Whit Monday"], ["2023-12-25", "Christmas Day"], ["2023-12-26", "St. Stephen's Day"],
        ["2024-01-01", "New Year's Day"], ["2024-03-29", "Good Friday"], ["2024-03-31", "Easter Sunday"],
        ["2024-04-01", "Easter Monday"], ["2024-04-27", "King's Birthday"], ["2024-05-04", "National Remembrance Day"],
        ["2024-05-05", "Liberation Day"], ["2024-05-09", "Ascension Day"], ["2024-05-19", "Whit Sunday"],
        ["2024-05-20", "Whit Monday"], ["2024-12-25", "Christmas Day"], ["2024-12-26", "St. Stephen's Day"]
    ]

    df['is_holiday'] = df["datetime_s"].dt.date.isin([pd.to_datetime(holiday[0]).date() for holiday in holidays_nl])
    df['weekday'] = df['datetime_s'].dt.dayofweek
    df['hour'] = df['datetime_s'].dt.hour

    df['duration'] = (df['datetime_e'] - df['datetime_s'])
    
    return df

def load_and_predict(model_path, input_data):
    model = load_model(model_path)
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
    try:
        # Construct the DataFrame with input data
        df = pd.DataFrame({
            'temperature': [temp],
            'rain_intensity': [rain],
            'streetname': [streetname],
            'gforce': [gforce],
            'speedlimit': [speedlimit],
            'windspeed': [windspeed],
            'datetime_s': pd.to_datetime(datetime),
            'datetime_e': pd.to_datetime(datetime),

            'event_cat': 1,
            'event_sev': 1,
            'speed': 10, 
            'end_speed': 20,
            'speed_limit': 50,
            'light_condition': 1,
            'duration_in_s': 10,
            'gforce': 5.4

        })

        # Add datetime features
        df = create_additional_datetime_features(df)

        # Load LabelEncoder classes
        classes_file_path = '/home/balage/Documents/BlockD/2023-24d-fai1-adsai-teamwork-t14/backend/api/assets/classes_streetname.npy'
        if os.path.exists(classes_file_path):
            encoder = LabelEncoder()
            encoder.classes_ = np.load(classes_file_path, allow_pickle=True)
        else:
            raise FileNotFoundError(f"File 'classes_streetname.npy' not found at '{classes_file_path}'.")

        # Transform streetname column using LabelEncoder
        df['streetname'] = df['streetname'].apply(lambda x: x if x in encoder.classes_ else 'Unknown')

        # Add 'Unknown' to encoder.classes_ if it doesn't exist
        if 'Unknown' not in encoder.classes_:
            encoder.classes_ = np.append(encoder.classes_, 'Unknown')

        df['streetname'] = encoder.transform(df['streetname'])

        print(df.head())
        # Extract input features for prediction
        input_data = df[['event_cat','event_sev','speed', 'end_speed', 'streetname', 'rain_intensity', 'temperature', 'windspeed', 'speed_limit', 'light_condition', 'is_holiday', 'weekday', 'hour', 'duration_in_s', 'gforce']].values

        # Ensure input_data is float32 (or int32 if applicable)
        input_data = input_data.astype('float32')

        # Load and predict using the model
        model_path = '/home/balage/Documents/BlockD/2023-24d-fai1-adsai-teamwork-t14/backend/api/assets/final_model_results_model.h5'  # Replace with actual path
        prediction = load_and_predict(model_path, input_data)

        return prediction[0]

    except Exception as e:
        # Log the exception or handle it appropriately
        print(f"An error occurred: {str(e)}")
        return None
    
class PredictionViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def make_predictions(self, request):
        try:
            temp = float(request.data.get('temp', 0))
            rain = float(request.data.get('rain', 0))
            streetname = request.data.get('streetname', '')
            gforce = float(request.data.get('gforce', 0))
            speedlimit = int(request.data.get('speedlimit', 0))
            windspeed = float(request.data.get('windspeed', 0))
            datetime = request.data.get('datetime', '')

            prediction = combine_functions(temp, rain, streetname, gforce, speedlimit, windspeed, datetime)

            # Check if prediction is valid (not NaN or infinite)
            if prediction is None or np.isnan(prediction) or np.isinf(prediction):
                raise ValueError("Invalid prediction value")

            response_data = {
                "prediction": float(prediction)  # Ensure prediction is converted to float explicitly
            }
            return Response(response_data)
        except Exception as e:
            # Log the exception or handle it appropriately
            print(f"An error occurred: {str(e)}")
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
