import preprocessing as preprocessing
from model_selection import save_model_results

from sklearn.metrics import classification_report, mean_squared_error, mean_absolute_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.svm import SVR

import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

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

def train_svr(X_train, y_train, X_val, y_val, kernel, C, epsilon):
    try:
        model = SVR(kernel=kernel, C=C, epsilon=epsilon)
        logger.info('Support Vector Regression model instantiated... ')
        logger.info(f"Parametres: kernel={kernel}, regularisation={C}, epsilon={epsilon}")
    
        model.fit(X_train, y_train)
        logger.info('Training finished... ')
    
        logger.info('Support Vector Vegression evaluation started... ')
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

# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main():
    try:
        logger.info("Started preprocessing...")
        X_train, X_val, y_train, y_val = preprocessing.main()

        # Define parameter grid
        kernels = ['linear', 'poly', 'rbf', 'sigmoid']
        C_values = [0.1, 1, 10, 100]
        epsilon_values = [0.01, 0.1, 1]

        # Save the best model
        best_model = None
        best_val_mse = float('inf')
        best_val_mae = float('inf')
        best_params = {}
        
        # Hyperparameter tuning
        logger.info("Started hyperparameter tuning...")
        for kernel in kernels:
            for C in C_values:
                for epsilon in epsilon_values:
                    model, train_mse, val_mse, train_mae, val_mae = train_svr(X_train, y_train, X_val, y_val, kernel, C, epsilon)
                    if val_mse < best_val_mse:
                        logger.info(f"New best model found: MSE = {val_mse}")
                        best_val_mse = val_mse
                        best_val_mae = val_mae
                        best_model = model
                        best_params = {'kernel': kernel, 'C': C, 'epsilon': epsilon}
        logger.info(f"Best parameters: {best_params}")
        
        # Saving the best model
        logger.info("Saving the best model...")
        save_model_results(model=best_model, train_data=X_train, val_mse=best_val_mse, val_mae=best_val_mae, filename='weights_files/svr_results.html')
    
    except Exception as e:
        logger.error('Something went wrong in the training step.')  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")


if __name__ == "__main__":
    main()