import preprocessing as preprocessing

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report, mean_squared_error, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
import xgboost as xgb

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

import numpy as np
import pandas as pd
import logging
import traceback
from joblib import dump
import json

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

def train_random_forest(X_train, y_train, X_val, y_val, n_estimators=100, random_state=None):
    """
    Train a Random Forest regressor model and evaluate its performance.

    This function trains a Random Forest regressor model using the training data (X_train, y_train)
    and evaluates its performance on the validation data (X_val, y_val). It calculates Mean Squared 
    Error (MSE) and Mean Absolute Error (MAE) for both training and validation sets. The function logs 
    messages for training, evaluation, and any errors encountered during the process.

    Parameters:
    -----------
    X_train : numpy.ndarray
        The training feature matrix.
    y_train : numpy.ndarray
        The training target vector.
    X_val : numpy.ndarray
        The validation feature matrix.
    y_val : numpy.ndarray
        The validation target vector.
    n_estimators : int, optional
        The number of trees in the Random Forest (default is 100).
    random_state : int or None, optional
        The random seed for reproducibility (default is None).

    Returns:
    --------
    model : RandomForestRegressor
        The trained Random Forest regressor model.
    train_mse : float
        Mean Squared Error (MSE) on the training set.
    val_mse : float
        Mean Squared Error (MSE) on the validation set.
    train_mae : float
        Mean Absolute Error (MAE) on the training set.
    val_mae : float
        Mean Absolute Error (MAE) on the validation set.

    Raises:
    -------
    TypeError
        If X_train, y_train, X_val, or y_val are not numpy arrays.
    ValueError
        If X_train and y_train, or X_val and y_val, do not have the same number of samples.
    Exception
        If any other unexpected error occurs during training and evaluation.
    """
    
    if not isinstance(X_train, np.ndarray) or not isinstance(y_train, np.ndarray):
        raise TypeError("X_train and y_train must be numpy arrays.")

    if X_train.shape[0] != len(y_train):
        raise ValueError("X_train and y_train must have the same number of samples.")

    if not isinstance(X_val, np.ndarray) or not isinstance(y_val, np.ndarray):
        raise TypeError("X_val and y_val must be numpy arrays.")

    if X_val.shape[0] != len(y_val):
        raise ValueError("X_val and y_val must have the same number of samples.")

    try:
        model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        
        logger.info('Regression Forest training started...')
        model.fit(X_train, y_train)
        logger.info('Regression Forest training finished')

        logger.info('Regression Forest evaluation started')
        train_predictions = model.predict(X_train)
        val_predictions = model.predict(X_val)

        train_mse = mean_squared_error(y_train, train_predictions)
        val_mse = mean_squared_error(y_val, val_predictions)
        train_mae = mean_absolute_error(y_train, train_predictions)
        val_mae = mean_absolute_error(y_val, val_predictions)

        return model, train_mse, val_mse, train_mae, val_mae

    except Exception as e:
        logger.error(f"An error occurred during training and evaluation: {str(e)}")
        raise

def train_xgboost_regression(X_train, y_train, X_val, y_val, params=None, num_boost_round=1000, early_stopping_rounds=50):
    """
    Train an XGBoost regression model and evaluate its performance.

    This function trains an XGBoost regression model using the training data (X_train, y_train) 
    and evaluates its performance on the validation data (X_val, y_val). It calculates Mean 
    Squared Error (MSE) and Mean Absolute Error (MAE) for both training and validation sets. 
    The function logs messages for training, evaluation, and any errors encountered during the process.

    Parameters:
    -----------
    X_train : numpy.ndarray
        The training feature matrix.
    y_train : numpy.ndarray
        The training target vector.
    X_val : numpy.ndarray
        The validation feature matrix.
    y_val : numpy.ndarray
        The validation target vector.
    params : dict, optional
        Parameters to be passed to the XGBoost model (default is None). If None, defaults to:
            'objective': 'reg:squarederror',  # Squared error for regression
            'eval_metric': 'rmse'             # Evaluation metric: Root Mean Squared Error (RMSE)
    num_boost_round : int, optional
        Number of boosting rounds (default is 1000).
    early_stopping_rounds : int, optional
        Activates early stopping. The model will train until validation score stops improving 
        for `early_stopping_rounds` rounds (default is 50).

    Returns:
    --------
    trained_model : xgboost.core.Booster
        The trained XGBoost regression model.
    train_mse : float
        Mean Squared Error (MSE) on the training set.
    val_mse : float
        Mean Squared Error (MSE) on the validation set.
    train_mae : float
        Mean Absolute Error (MAE) on the training set.
    val_mae : float
        Mean Absolute Error (MAE) on the validation set.

    Raises:
    -------
    TypeError
        If X_train, y_train, X_val, or y_val are not numpy arrays.
    ValueError
        If X_train and y_train, or X_val and y_val, do not have the same number of samples.
    Exception
        If any other unexpected error occurs during training and evaluation.
    """

    if not isinstance(X_train, np.ndarray) or not isinstance(y_train, np.ndarray):
        raise TypeError("X_train and y_train must be numpy arrays.")

    if X_train.shape[0] != len(y_train):
        raise ValueError("X_train and y_train must have the same number of samples.")

    if not isinstance(X_val, np.ndarray) or not isinstance(y_val, np.ndarray):
        raise TypeError("X_val and y_val must be numpy arrays.")

    if X_val.shape[0] != len(y_val):
        raise ValueError("X_val and y_val must have the same number of samples.")

    try:
        if params is None:
            params = {
                'objective': 'reg:squarederror',  # Squared error for regression
                'eval_metric': 'rmse'             # Evaluation metric: Root Mean Squared Error (RMSE)
            }
        
        # Convert data into DMatrix format for XGBoost
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dval = xgb.DMatrix(X_val, label=y_val)
        
        # Specify validation set to watch performance
        watchlist = [(dtrain, 'train'), (dval, 'eval')]
        
        # Train the XGBoost model
        trained_model = xgb.train(params, dtrain, num_boost_round=num_boost_round,
                                  evals=watchlist, early_stopping_rounds=early_stopping_rounds, verbose_eval=10)
        
        # Make predictions on the training and validation sets
        y_train_pred = trained_model.predict(dtrain)
        y_val_pred = trained_model.predict(dval)
        
        # Evaluate the model
        train_mse = mean_squared_error(y_train, y_train_pred)
        val_mse = mean_squared_error(y_val, y_val_pred)
        train_mae = mean_absolute_error(y_train, y_train_pred)
        val_mae = mean_absolute_error(y_val, y_val_pred)
        
        # Return trained model and evaluation metrics
        return trained_model, train_mse, val_mse, train_mae, val_mae
        
    except Exception as e:
        logger.error(f"An error occurred during training and evaluation: {str(e)}")
        raise

def train_neural_network(X_train, y_train, X_val, y_val, epochs=20, batch_size=64, patience=4, 
                         hidden_layers=[64, 32], learning_rate=0.01):
    """
    Train a feedforward neural network regression model using TensorFlow/Keras.

    This function trains a feedforward neural network regression model using the training data (X_train, y_train)
    and evaluates its performance on the validation data (X_val, y_val). It uses Mean Squared Error (MSE) as the
    loss function and Adam optimizer for training. The function logs messages for training start, training finish,
    and any errors encountered during the process.

    Parameters:
    -----------
    X_train : numpy.ndarray
        The training feature matrix.
    y_train : numpy.ndarray
        The training target vector.
    X_val : numpy.ndarray
        The validation feature matrix.
    y_val : numpy.ndarray
        The validation target vector.
    epochs : int, optional
        Number of epochs for training (default is 20).
    batch_size : int, optional
        Number of samples per gradient update (default is 64).
    patience : int, optional
        Number of epochs with no improvement after which training will be stopped if `early_stopping` is used
        (default is 4).
    hidden_layers : list of int, optional
        List specifying the number of units in each hidden layer (default is [64, 32]).
    learning_rate : float, optional
        Learning rate for the Adam optimizer (default is 0.01).

    Returns:
    --------
    model : tf.keras.models.Sequential
        The trained neural network model.
    history : tf.keras.callbacks.History
        History object containing training metrics.

    Raises:
    -------
    TypeError
        If X_train, y_train, X_val, or y_val are not numpy arrays.
    ValueError
        If X_train and y_train, or X_val and y_val, do not have the same number of samples.
    Exception
        If any other unexpected error occurs during training and evaluation.
    """

    if not isinstance(X_train, np.ndarray) or not isinstance(y_train, np.ndarray):
        raise TypeError("X_train and y_train must be numpy arrays.")

    if X_train.shape[0] != len(y_train):
        raise ValueError("X_train and y_train must have the same number of samples.")

    if not isinstance(X_val, np.ndarray) or not isinstance(y_val, np.ndarray):
        raise TypeError("X_val and y_val must be numpy arrays.")

    if X_val.shape[0] != len(y_val):
        raise ValueError("X_val and y_val must have the same number of samples.")

    try:
        # Enable memory growth
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)
    
        # Clear session
        tf.keras.backend.clear_session()
    
        model = Sequential()
        # Add input layer
        model.add(Dense(hidden_layers[0], activation='relu', input_shape=(X_train.shape[1],)))
    
        # Add hidden layers
        for units in hidden_layers[1:]:
            model.add(Dense(units, activation='relu'))
        
        # Add output layer
        model.add(Dense(1))
    
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(loss='mean_squared_error', optimizer=optimizer)
        logger.info('Neural Network has been compiled')
    
        early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)
    
        logger.info('Neural Network training started...')
        history = model.fit(
            X_train, 
            y_train, 
            epochs=epochs, 
            batch_size=batch_size, 
            validation_data=(X_val, y_val),
            callbacks=[early_stopping],
            verbose=1
        )
        logger.info('Neural Network training finished')
    
        # Clear session
        tf.keras.backend.clear_session()
    
        return model, history
        
    except Exception as e:
        logger.error(f"An error occurred during training and evaluation: {str(e)}")
        raise

def save_model_results(model, train_data=None, history=None, train_mse=None, val_mse=None, train_mae=None, val_mae=None, filename='model_results.html'):
    """
    Save the results of a machine learning model training and evaluation to an HTML file.

    This function writes an HTML file with the model type, feature importances (if applicable), training and
    validation scores (MSE and MAE), and optionally training history for Keras models. The file also includes
    saving the model itself using native serialization methods (e.g., XGBoost model) or Keras's `.h5` format.

    Parameters:
    -----------
    model : object
        The trained machine learning model.
    train_data : numpy.ndarray or None, optional
        Training data used for the model (default is None).
    history : tf.keras.callbacks.History or None, optional
        History object from Keras training (default is None).
    train_mse : float or None, optional
        Mean Squared Error (MSE) score on training data (default is None).
    val_mse : float or None, optional
        Mean Squared Error (MSE) score on validation data (default is None).
    train_mae : float or None, optional
        Mean Absolute Error (MAE) score on training data (default is None).
    val_mae : float or None, optional
        Mean Absolute Error (MAE) score on validation data (default is None).
    filename : str, optional
        File name to save the results (default is 'model_results.html').

    Raises:
    -------
    TypeError
        If the type of `model` is not recognized (not XGBoost, RandomForestRegressor, or Keras model).
    Exception
        If any unexpected error occurs during the file writing process.
    """

    with open(filename, 'w') as file:
        file.write("<html><head><title>Model Results</title></head><body>\n")
        
        file.write("<h2>Model Type:</h2>\n")
        file.write(f"<p>{type(model)}</p>\n\n")
        logger.debug(type(model))

        if isinstance(model, xgb.Booster):  # For XGBoost models
            file.write("<h2>Feature Importances:</h2>\n")
            if train_data is not None:
                df = pd.DataFrame(train_data, columns=['datetime_s', 'datetime_e', 'event_cat', 'event_sev', 'speed', 'end_speed', 'maxwaarde', 'streetname', 'rain_intensity', 'temperature', 'windspeed', 'speed_limit', 'light_condition', 'accident_sev', 'accident_prob'])
                importances = pd.DataFrame({'Feature': df.columns, 'Importance': model.get_score(importance_type='weight').values()})
                file.write(importances.to_html(index=False))

            file.write(f"<h2>Training Score (MSE):</h2> <p>{train_mse}</p>\n")
            file.write(f"<h2>Validation Score (MSE):</h2> <p>{val_mse}</p>\n")
            file.write(f"<h2>Training Score (MAE):</h2> <p>{train_mae}</p>\n")
            file.write(f"<h2>Validation Score (MAE):</h2> <p>{val_mae}</p>\n")
            
            # Save the model using native XGBoost serialization
            model.save_model(filename.replace(".html", "_model.json"))

        elif isinstance(model, RandomForestRegressor):  # For random forest
            file.write("<h2>Feature Importances:</h2>\n")
            if train_data is not None:
                df = pd.DataFrame(train_data, columns=['datetime_s', 'datetime_e', 'event_cat', 'event_sev', 'speed', 'end_speed', 'maxwaarde', 'streetname', 'rain_intensity', 'temperature', 'windspeed', 'speed_limit', 'light_condition', 'accident_sev', 'accident_prob'])
                importances = pd.DataFrame({'Feature': df.columns, 'Importance': model.feature_importances_})
                file.write(importances.to_html(index=False))

            file.write(f"<h2>Training Score (MSE):</h2> <p>{train_mse}</p>\n")
            file.write(f"<h2>Validation Score (MSE):</h2> <p>{val_mse}</p>\n")
            file.write(f"<h2>Training Score (MAE):</h2> <p>{train_mae}</p>\n")
            file.write(f"<h2>Validation Score (MAE):</h2> <p>{val_mae}</p>\n")

        elif 'keras' in str(type(model)):  # For Keras models
            if history is not None:
                file.write("<h2>Training History:</h2>\n")
                history_df = pd.DataFrame(history.history)
                file.write(history_df.to_html(index=False))

            file.write(f"<h2>Training Score (MSE):</h2> <p>{train_mse}</p>\n")
            file.write(f"<h2>Validation Score (MSE):</h2> <p>{val_mse}</p>\n")
            file.write(f"<h2>Training Score (MAE):</h2> <p>{train_mae}</p>\n")
            file.write(f"<h2>Validation Score (MAE):</h2> <p>{val_mae}</p>\n")
            
            # Save the Keras model
            model.save(filename.replace(".html", "_model.h5"))

        file.write("</body></html>\n")

# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main():
    try:
        logger.info("Started preprocessing...")
        X_train, X_val, y_train, y_val = preprocessing.main()
        nn, history = train_neural_network(X_train, y_train, X_val, y_val)
        xgboost, xg_train_mse, xg_val_mse, xg_train_mae, xg_val_mae = train_xgboost_regression(X_train, y_train, X_val, y_val)
        rfr, rf_train_mse, rf_val_mse, rf_train_mae, rf_val_mae = train_random_forest(X_train, y_train, X_val, y_val)
        save_model_results(nn, history=history, filename='weights_files/neuralnetwork_results.html')
        save_model_results(xgboost, train_data=X_train, train_mse=xg_train_mse, val_mse=xg_val_mse, train_mae=xg_train_mae, val_mae=xg_val_mae, filename='weights_files/xgboost_results.html')
        save_model_results(rfr, train_data=X_train, train_mse=rf_train_mse, val_mse=rf_val_mse, train_mae=rf_train_mae, val_mae=rf_val_mae, filename='weights_files/randomforest_results.html')
    except Exception as e:
        logger.error('Something went wrong in the training step.')  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")

if __name__ == "__main__":
    main()
    