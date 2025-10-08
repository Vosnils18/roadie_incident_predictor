import feature_eng as feature_eng

import datetime as dt
import logging
import traceback
import json

import psycopg2
import numpy as np
import pandas as pd
import pickle

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


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

# Function for connecting to the database
def connection_db(path_to_json):
    """
    Establish a connection to a PostgreSQL database using configuration parameters from a JSON file.

    This function loads database connection parameters from a specified JSON file and attempts to 
    establish a connection to a PostgreSQL database using these parameters. It returns the connection 
    object and cursor if successful, and logs an appropriate message.

    Parameters:
    -----------
    path_to_json : str
        The file path to the JSON file containing the database connection parameters.

    Returns:
    --------
    conn : psycopg2.extensions.connection
        The connection object for the PostgreSQL database.
    cursor : psycopg2.extensions.cursor
        The cursor object for the PostgreSQL database.

    Raises:
    -------
    OperationalError
        If the connection to the database could not be established, an OperationalError is raised and
        an error message is logged.

    Example JSON file structure:
    ----------------------------
    .. code-block:: json
    
        {
            "dbname": "your_database_name",
            "user": "your_username",
            "password": "your_password",
            "host": "your_host",
            "port": "your_port"
        }
    """
    
    with open(path_to_json) as config_file:
        db_params = json.load(config_file)
 
    # Connect to the database
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        logger.info('Connection to database established')
        return conn, cursor
    except OperationalError as e:
        logger.error('Connection to database could not be established.')

# Function for fetching the data from the connected database
def fetch_data(conn, cursor, get_head=False):
    """
    Fetch data from the connected PostgreSQL database and load it into a pandas DataFrame.

    This function executes a SQL query to retrieve all records from the 'group14_warehouse.regression_data'
    table. The results are loaded into a pandas DataFrame with specified column names. The connection 
    to the database is closed after fetching the data. Optionally, it can print the first few rows of the 
    DataFrame.

    Parameters:
    -----------
    conn : psycopg2.extensions.connection
        The connection object for the PostgreSQL database.
    cursor : psycopg2.extensions.cursor
        The cursor object for the PostgreSQL database.
    get_head : bool, optional
        If True, prints the first few rows of the DataFrame (default is False).

    Returns:
    --------
    pandas.DataFrame
        DataFrame containing the data fetched from the database with the specified column names.
    """
    get_data = '''SELECT * FROM group14_warehouse.regression_data'''

    cursor.execute(get_data)
    logger.info('Data pulled from warehouse')
    df = pd.DataFrame(cursor.fetchall(), columns=['datetime_s', 'datetime_e', 'event_cat', 'event_sev', 'speed', 'end_speed',
                                                  'maxwaarde', 'streetname', 'rain_intensity', 'temperature', 'windspeed',
                                                  'speed_limit', 'light_condition', 'accident_sev', 'accident_prob'])
    
    print(df.head())
    conn.close()
    logger.info('Connection to database closed')
    return df

def remove_outliers(df):
    """
    Remove outliers from the DataFrame based on the 'accident_prob' column.

    This function filters out rows in the input DataFrame where the value in the 'accident_prob' 
    column exceeds a specified threshold. Specifically, it removes rows where 'accident_prob' is greater 
    than 100.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing an 'accident_prob' column.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with rows where 'accident_prob' exceeds 100 removed.
    """
    
    # Filter out rows where the value in the specified column exceeds the threshold
    df = df[df['accident_prob'] <= 100]
    return df

def fix_dtypes(df, cats, dats):
    """
    Fix data types for datetime and categorical columns in the DataFrame.

    This function converts specified columns to datetime and categorical types. 
    The datetime columns are converted using `pd.to_datetime`, and the categorical 
    columns are encoded using `LabelEncoder`.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame with columns to be converted.
    cats : list of str
        List of column names to be converted to categorical types and encoded.
    dats : list of str
        List of column names to be converted to datetime types.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with specified columns converted to appropriate types.
    """
    logger.debug("fixing Dtypes...")
    for column in dats: # Loop through dtatime columns
        df[column] = pd.to_datetime(df[column])
    
    for column in cats: # Loop through categorical columns
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        if column == 'streetname':
            np.save('weights_files/classes_streetname.npy', encoder.classes_)
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.

    This function identifies and removes duplicate rows from the input DataFrame. 
    It keeps only the unique rows and removes all duplicates.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame from which duplicate rows need to be removed.

    Returns:
    --------
    pandas.DataFrame
        The input DataFrame with duplicate rows removed.
    """
    logger.debug("Removing duplicates")
    duplicates = df.duplicated(keep=False)
    df = df[~duplicates]
    return df

# Function to create X and y
def create_xy(df):
    """
    Create feature matrix X and target vectors y and y_sev from the DataFrame.

    This function separates the input DataFrame into features (X) and target variables (y and y_sev).
    The features matrix X is created by dropping the 'accident_sev' and 'accident_prob' columns from 
    the DataFrame. The target vectors y and y_sev are the 'accident_prob' and 'accident_sev' columns, 
    respectively.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame containing feature columns and target columns 'accident_sev' and 'accident_prob'.

    Returns:
    --------
    X : pandas.DataFrame
        The feature matrix, created by dropping 'accident_sev' and 'accident_prob' from the input DataFrame.
    y : pandas.Series
        The target vector for 'accident_prob'.
    y_sev : pandas.Series
        The target vector for 'accident_sev'.
    """
    logger.debug("Creating X and Y")
    X = df.drop(['accident_sev', 'accident_prob'], axis=1)
    logger.debug(X.dtypes)
    y = df['accident_prob']

    return X, y

# Function to split the data into training, validation and testing partitions
def split_tvt(X, y):
    """
    Split the data into training, validation, and testing partitions.

    This function splits the feature matrix X and target vector y into training, validation, 
    and testing sets. It performs two splits: first to create the training and testing sets, 
    and then to split the training set further into training and validation sets. The function 
    ensures that there are enough samples in each partition and logs the shapes of the resulting 
    datasets.

    Parameters:
    -----------
    X : pandas.DataFrame
        The feature matrix.
    y : pandas.Series
        The target vector.

    Returns:
    --------
    X_train : pandas.DataFrame
        The training feature matrix.
    X_val : pandas.DataFrame
        The validation feature matrix.
    X_test : pandas.DataFrame
        The testing feature matrix.
    y_train : pandas.Series
        The training target vector.
    y_val : pandas.Series
        The validation target vector.
    y_test : pandas.Series
        The testing target vector.

    Raises:
    -------
    ValueError
        If the number of samples in X is too small to split or if the number of samples 
        in the training set is too small after the test split.
    """
    if X.shape[0] < 2:
        raise ValueError("The number of samples in X is too small to split.")
    
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.2,  # Adjust as needed
                                                        random_state=0)

    if X_train.shape[0] < 2:
        raise ValueError("The number of samples in X_train is too small after test split.")
    
    X_train, X_val, y_train, y_val = train_test_split(X_train,
                                                      y_train,
                                                      test_size=1/9,  # Adjust as needed
                                                      random_state=0)

    logger.info("X_train shape: %s || y_train shape: %s", X_train.shape, y_train.shape)
    logger.info("X_val shape: %s || y_val shape: %s", X_val.shape, y_val.shape)
    logger.info("X_test shape: %s || y_test shape: %s", X_test.shape, y_test.shape)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def normalize_data(X_train, X_val=None, X_test=None, scaler=None):
    """
    Normalize the data using a scaler across training, validation, and testing partitions.

    This function normalizes the data using a scaler across training, validation, and testing partitions.
    If no scaler is provided, it initializes a `StandardScaler` and fits it on the training data. It then
    transforms the data for all partitions using the fitted scaler.

    Parameters:
    -----------
    X_train : numpy.ndarray or pandas.DataFrame
        The training feature matrix to be normalized.
    X_val : numpy.ndarray or pandas.DataFrame, optional
        The validation feature matrix to be normalized (default is None).
    X_test : numpy.ndarray or pandas.DataFrame, optional
        The testing feature matrix to be normalized (default is None).
    scaler : sklearn-like scaler object, optional
        The scaler object used to normalize the data (default is None).

    Returns:
    --------
    X_train_norm : numpy.ndarray
        The normalized training feature matrix.
    X_val_norm : numpy.ndarray or None
        The normalized validation feature matrix, or None if X_val is None.
    X_test_norm : numpy.ndarray or None
        The normalized testing feature matrix, or None if X_test is None.
    scaler : sklearn-like scaler object
        The scaler object fitted on the training data, used for normalization.
    """
    
    if scaler is None:
        scaler = StandardScaler()
        scaler.fit(X_train)

    X_train_norm = scaler.transform(X_train)
    X_val_norm = scaler.transform(X_val) if X_val is not None else None
    X_test_norm = scaler.transform(X_test) if X_test is not None else None

    return X_train_norm, X_val_norm, X_test_norm, scaler

# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main():
    try:
        json_path = '../db_config.json'
        conn, cursor = connection_db(json_path)
        data = fetch_data(conn, cursor, True)
        data = remove_outliers(data)
        data = remove_duplicates(data)
        data = fix_dtypes(data, ['event_cat', 'event_sev', 'streetname', 'light_condition', 'accident_sev'], ['datetime_s', 'datetime_e'])
        logger.info("feature engineering started...")
        data = feature_eng.main(data)
        X, y = create_xy(data)
        logger.debug("created X and y")
        X_train, X_val, X_test, y_train, y_val, y_test = split_tvt(X, y)
        logger.debug("split the data")
        logger.debug(pd.DataFrame(X_train).dtypes)
        X_train, X_val, X_test, scaler = normalize_data(X_train, X_val, X_test)
        logger.info("Data preprocessing and split done.")
        return X_train, X_val, y_train, y_val
    except Exception as e:
        logger.error("Something went wrong in the preprocessing step.")  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")

if __name__ == "__main__":
    main()