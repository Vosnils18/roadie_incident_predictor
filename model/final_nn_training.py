import preprocessing as preprocessing
import model_selection as model_selection
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.regularizers import l2

import numpy as np
import pandas as pd
import logging
import traceback
import pickle
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

def train_neural_network(X_train, y_train, X_val, y_val, epochs=20, batch_size=64, patience=10, 
                         learning_rate=0.1):
    """
    Train a neural network model using TensorFlow/Keras.

    Parameters:
    -----------
    X_train : numpy.ndarray
        Training data features.
    y_train : numpy.ndarray
        Training data labels.
    X_val : numpy.ndarray
        Validation data features.
    y_val : numpy.ndarray
        Validation data labels.
    epochs : int, optional
        Number of epochs to train the model (default is 20).
    batch_size : int, optional
        Number of samples per gradient update (default is 64).
    patience : int, optional
        Number of epochs with no improvement after which training will be stopped (default is 10).
    learning_rate : float, optional
        Learning rate for the Adam optimizer (default is 0.1).

    Returns:
    --------
    model : tf.keras.Model
        Trained neural network model.
    history : tf.keras.callbacks.History
        History object containing training metrics.
    """

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

    # Define the model
    model = Sequential()
    
    # Input layer
    model.add(Dense(256, input_shape=(X_train.shape[1],)))
    model.add(LeakyReLU(alpha=0.1))
    model.add(BatchNormalization())
    
    # Hidden layers
    model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    model.add(Dense(32, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dropout(0.5))
    model.add(BatchNormalization())
    
    # Output layer for regression
    model.add(Dense(1))
    
    # Compile the model
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss='mean_squared_error', metrics=['mean_absolute_error'])
    logger.info('Neural Network has been compiled')
    
    # Callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=patience, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)


    logger.info('Neural Network training started...')
    history = model.fit(
        X_train, 
        y_train, 
        epochs=epochs, 
        batch_size=batch_size, 
        validation_data=(X_val, y_val),
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )
    logger.info('Neural Network training finished')

    # Clear session
    tf.keras.backend.clear_session()

    return model, history

# ------------------------------------------------------------------------------------------------------------------------ #
#                                                                                                                          #
#                                                           Main                                                           #
#                                                                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #

def main():
    try:
        logger.info("Started preprocessing...")
        X_train, X_val, y_train, y_val = preprocessing.main()
        nn, history = train_neural_network(X_train, y_train, X_val, y_val, epochs=100)
        model_selection.save_model_results(nn, history=history, filename='weights_files/final/final_model_results.html')
    except Exception as e:
        logger.error('Something went wrong in the training step.')  
        logger.error(F"Exception: {e}\nTraceback: \n{traceback.format_exc()}")

if __name__ == "__main__":
    main()