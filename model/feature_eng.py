import datetime as dt
import logging
import traceback
import json

import psycopg2
import numpy as np
import pandas as pd

# Create a logger object
logger = logging.getLogger(__name__)

# Set the logging level to DEBUG
logger.setLevel(logging.DEBUG)

# Create a console handler to output logs to the terminal
console_handler = logging.StreamHandler()

# Set the format for the log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)
 
# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Functions                                                      #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def create_additional_datetime_features(df):
    """
    Add additional datetime-related features to the DataFrame.

    This function enriches the input DataFrame by computing various datetime-related features
    based on the columns 'datetime_s' (start datetime) and 'datetime_e' (end datetime). 
    The new features added include:
    - 'is_holiday': Boolean indicating if the date is a Dutch national holiday.
    - 'weekday': Day of the week represented as an integer (0 = Monday, 6 = Sunday).
    - 'hour': Hour of the day (0-23).
    - 'duration': Duration between 'datetime_s' and 'datetime_e' as a timedelta.
    - 'duration_in_s': Duration in seconds as an integer.

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

    Notes:
    ------
    The list of Dutch national holidays is hardcoded for the years 2018-2024.
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
    ] # List provided by blackbox.ai, confirmed on www.government.nl

    df['is_holiday'] = df["datetime_s"].dt.date.isin([pd.to_datetime(holiday[0]).date() for holiday in holidays_nl]) # Check if date is a holiday.
    df['weekday'] = df['datetime_s'].dt.dayofweek
    df['hour'] = df['datetime_s'].dt.hour

    df['duration'] = df['datetime_e'] - df['datetime_s']
    df['duration_in_s'] = df['duration'].dt.total_seconds().astype(int) # Calculate duration in seconds (existing column is inconsistent)
    return df

def calculate_gforce(df):
    """
    Calculate the g-force for events in the DataFrame.

    This function calculates the g-force experienced during events recorded in the input DataFrame.
    It differentiates between events categorized as 'event_cat' 3 (where 'maxwaarde' represents speed)
    and other events (where 'maxwaarde' represents g-force). For non-speed events, it calculates the g-force
    based on the change in speed and the duration of the event.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing at least the columns 'event_cat', 'maxwaarde', 'speed', 
        'maxspeed', 'duration_in_s', and 'gforce'.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with updated 'gforce' values and intermediate calculation columns removed.

    Process:
    --------
    1. For events with 'event_cat' == 3, 'maxwaarde' is assigned to 'maxspeed'.
    2. For events with 'event_cat' != 3, 'maxwaarde' is assigned to 'gforce'.
    3. Calculate the change in speed ('delta_v') as the difference between 'maxspeed' and 'speed'.
    4. Calculate the acceleration ('acceleration') as 'delta_v' divided by 'duration_in_s'.
    5. Calculate the g-force ('calculated_gforce') as 'acceleration' divided by 9.81.
    6. Fill NaN values in the original 'gforce' column with 'calculated_gforce'.
    7. Drop the intermediate calculation columns ('delta_v', 'acceleration', 'calculated_gforce').

    Notes:
    ------
    - The function assumes the input DataFrame has been pre-processed with the 'duration_in_s' column
      correctly calculated as the duration in seconds.
    - The gravitational constant used for calculating g-force is 9.81 m/s².
    """
    
    df.loc[df['event_cat'] == 3, 'maxspeed'] = df['maxwaarde']
    df.loc[df['event_cat'] != 3, 'gforce'] = df['maxwaarde']

    # Calculate the change in speed
    df['delta_v'] = df['maxspeed'] - df['speed']
    # Calculate the acceleration
    df['acceleration'] = df['delta_v'] / df['duration_in_s']
    # Calculate the g-force
    df['calculated_gforce'] = df['acceleration'] / 9.81
    # Fill NaN values in the original gforce column with the calculated values
    df['gforce'] = df['gforce'].fillna(df['calculated_gforce'])
    
    # Drop the columns used for calculation
    df = df.drop(columns=['delta_v', 'acceleration', 'calculated_gforce', ])
    
    return df

def set_speed_limit(df):
    """
    Clean and convert the 'speed_limit' column in the DataFrame.

    This function processes the 'speed_limit' column by replacing non-numeric values ("Un" and "No")
    with "0", and then converting the column to integer type. Rows where 'speed_limit' cannot be 
    converted to a numeric value even after replacements are dropped.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing a 'speed_limit' column with mixed data types that need to be cleaned 
        and converted to integers.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with the 'speed_limit' column cleaned and converted to integers. Rows 
        with non-numeric 'speed_limit' values after replacements are dropped.

    Process:
    --------
    1. Replace "Un" with "0" in the 'speed_limit' column.
    2. Replace "No" with "0" in the 'speed_limit' column.
    3. Drop rows where 'speed_limit' is not numeric after the replacements.
    4. Convert the 'speed_limit' column to integer type.
    """
    # Replace "Un" with "0" 
    df['speed_limit'] = df['speed_limit'].astype(str).str.replace("Un", "0", regex=False) 
    # Replace "No" with "0"
    df['speed_limit'] = df['speed_limit'].astype(str).str.replace("No", "0", regex=False)

    # Drop rows where speed_limit is still not numeric after the replacements
    # this will allow us to convert it back to an int
    df = df[pd.to_numeric(df['speed_limit'], errors='coerce').notnull()]

    # Convert speed_limit back to integer 
    df['speed_limit'] = df['speed_limit'].astype(int)
    
    return df

# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main(data):
    try:
        logger.debug(data.head())
        logger.debug("setting speed limit...")
        data = set_speed_limit(data)
        logger.debug("creating aditional datetime features...")
        data = create_additional_datetime_features(data)
        logger.debug("Calculating Gforce...")
        data = calculate_gforce(data)
        logger.debug("Dropping leftover columns")
        data = data.drop(['datetime_s', 'datetime_e', 'maxwaarde', 'duration', 'maxspeed'], axis=1)
        logger.debug("Leftover columns: ", data.columns, data.dtypes)
        logger.info("Feature Engineering Done")
        return data
    except Exception as e:
        logger.error("Something went wrong in the feature engineering step.")  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")
    
if __name__ == "__main__":
    main()