import preprocessing as preprocessing
import model_selection as model_selection
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from scipy.stats import uniform, randint

import numpy as np
import pandas as pd
import logging
import traceback
import joblib
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

def train_xgboost_regression(X_train, y_train, X_val, y_val, params=None, num_boost_round=1000, early_stopping_rounds=50, n_iter=50, n_jobs=-1):
    """
    Trains an XGBoost regressor using randomized search for hyperparameter optimization
    and early stopping based on validation performance.

    Parameters:
    -----------
    X_train : numpy.ndarray
        Training data features of shape (n_samples, n_features).
    y_train : numpy.ndarray
        Training data labels of shape (n_samples,).
    X_val : numpy.ndarray
        Validation data features of shape (n_samples, n_features).
    y_val : numpy.ndarray
        Validation data labels of shape (n_samples,).
    params : dict, optional
        Parameters for XGBoost regressor. If None, default parameters are used:
        {'objective': 'reg:squarederror', 'eval_metric': 'rmse'}.
    num_boost_round : int, optional
        Number of boosting rounds (trees) to train. Default is 1000.
    early_stopping_rounds : int, optional
        Activates early stopping. Validation performance needs to improve at least
        once in every early_stopping_rounds round(s) to continue training. Default is 50.
    n_iter : int, optional
        Number of parameter settings that are sampled in randomized search. Default is 50.
    n_jobs : int, optional
        Number of jobs to run in parallel for randomized search. -1 means using all processors.
        Default is -1.

    Returns:
    --------
    best_model : xgboost.sklearn.XGBRegressor
        Best trained XGBoost regressor model based on validation performance.
    train_mse : float
        Mean squared error (MSE) of the training set predictions.
    val_mse : float
        Mean squared error (MSE) of the validation set predictions.
    train_mae : float
        Mean absolute error (MAE) of the training set predictions.
    val_mae : float
        Mean absolute error (MAE) of the validation set predictions.
    """
    
    if params is None:
        params = {
            'objective': 'reg:squarederror',
            'eval_metric': 'rmse'
        }
    
    # Define hyperparameter search space
    param_distributions = {
        'learning_rate': uniform(0.01, 0.3),
        'max_depth': randint(3, 10),
        'min_child_weight': randint(1, 10),
        'subsample': uniform(0.5, 0.5),
        'colsample_bytree': uniform(0.5, 0.5),
        'n_estimators': randint(100, 1000)
    }
    
    xgb_model = xgb.XGBRegressor(**params)
    
    # Randomized search with cross-validation
    random_search = RandomizedSearchCV(estimator=xgb_model, param_distributions=param_distributions, 
                                       n_iter=n_iter, scoring='neg_mean_squared_error', 
                                       cv=3, verbose=1, n_jobs=n_jobs, random_state=42)
    
    random_search.fit(X_train, y_train)
    
    # Retrieve the best parameters and model
    best_params = random_search.best_params_
    best_model = random_search.best_estimator_
    
    # Train the best model with early stopping
    best_model.set_params(eval_metric='rmse')
    best_model.fit(X_train, y_train, 
                   eval_set=[(X_train, y_train), (X_val, y_val)],
                   early_stopping_rounds=early_stopping_rounds, verbose=True)
    
    # Make predictions on the training and validation sets
    y_train_pred = best_model.predict(X_train)
    y_val_pred = best_model.predict(X_val)
    
    # Evaluate the model
    train_mse = mean_squared_error(y_train, y_train_pred)
    val_mse = mean_squared_error(y_val, y_val_pred)
    train_mae = mean_absolute_error(y_train, y_train_pred)
    val_mae = mean_absolute_error(y_val, y_val_pred)
    
    # Return trained model and evaluation metrics
    return best_model, train_mse, val_mse, train_mae, val_mae
# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main():
    try:
        logger.info("Started preprocessing...")
        X_train, X_val, y_train, y_val = preprocessing.main()
        xgboost, xg_train_mse, xg_val_mse, xg_train_mae, xg_val_mae = train_xgboost_regression(X_train, y_train, X_val, y_val)
        model_selection.save_model_results(xgboost, train_data=X_train, train_mse=xg_train_mse, val_mse=xg_val_mse, train_mae=xg_train_mae, val_mae=xg_val_mae, filename='weights_files/final/final_xgboost_results.html')
    except Exception as e:
        logger.error('Something went wrong in the training step.')  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")

if __name__ == "__main__":
    main()