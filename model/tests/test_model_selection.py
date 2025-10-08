import pytest
import numpy as np
from unittest.mock import MagicMock, patch

import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

from model.model_selection import (train_random_forest, 
                                   train_xgboost_regression, 
                                   train_neural_network, 
                                   save_model_results)

def test_train_random_forest():
    # Generate some random data
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Call the function
    model, train_mse, val_mse, train_mae, val_mae = train_random_forest(X_train, y_train, X_val, y_val)

    # Assertions
    assert isinstance(model, RandomForestRegressor)
    assert train_mse >= 0 
    assert val_mse >= 0
    assert train_mae >= 0
    assert val_mae >= 0

def test_train_xgboost_regression():
    # Generate some random data
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Call the function
    trained_model, train_mse, val_mse, train_mae, val_mae = train_xgboost_regression(X_train, y_train, X_val, y_val)

    # Assertions
    assert isinstance(trained_model, xgb.Booster)
    assert train_mse >= 0  # Assuming MSE is non-negative
    assert val_mse >= 0
    assert train_mae >= 0
    assert val_mae >= 0

def test_train_neural_network():
    # Generate some random data
    X, y = make_regression(n_samples=100, n_features=10, noise=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Call the function
    model, history = train_neural_network(X_train, y_train, X_val, y_val)

    # Assertions
    assert isinstance(model, Sequential)
    assert isinstance(history, tf.keras.callbacks.History)
    assert len(history.history['loss']) > 0  # Ensure there was at least one training step
    assert len(history.history['val_loss']) > 0  # Ensure there was at least one validation step


@pytest.fixture
def mock_model():
    return MagicMock()

@pytest.fixture
def mock_history():
    return MagicMock()

@pytest.fixture
def mock_train_data():
    return np.random.rand(100, 10)  # Mocking training data

@pytest.fixture
def mock_metrics():
    return {
        'train_mse': 0.1,
        'val_mse': 0.2,
        'train_mae': 0.3,
        'val_mae': 0.4
    }

def test_save_model_results_xgb(mock_model, mock_train_data, mock_metrics):
    with patch('builtins.open', create=True) as mock_open:
        # Mocking XGBoost model type
        type(mock_model).__module__ = 'xgboost.core'  # Simulate type of XGBoost model
        save_model_results(mock_model, train_data=mock_train_data, **mock_metrics)

        # Assertions
        handle = mock_open.return_value.__enter__.return_value
        assert handle.write.call_count > 0
        written_content = ''.join([args[0] for args, kwargs in handle.write.call_args_list])

def test_save_model_results_rf(mock_model, mock_train_data, mock_metrics):
    with patch('builtins.open', create=True) as mock_open:
        # Mocking RandomForestRegressor model type
        type(mock_model).__name__ = 'RandomForestRegressor'  # Simulate type of RandomForestRegressor model
        save_model_results(mock_model, train_data=mock_train_data, **mock_metrics)

        # Assertions
        handle = mock_open.return_value.__enter__.return_value
        assert handle.write.call_count > 0
        written_content = ''.join([args[0] for args, kwargs in handle.write.call_args_list])

def test_save_model_results_keras(mock_model, mock_history, mock_metrics):
    with patch('builtins.open', create=True) as mock_open:
        # Mocking Keras model type
        type(mock_model).__module__ = 'tensorflow.python.keras.engine.sequential'  # Simulate type of Keras model
        save_model_results(mock_model, history=mock_history, **mock_metrics)

        # Assertions
        handle = mock_open.return_value.__enter__.return_value
        assert handle.write.call_count > 0
        written_content = ''.join([args[0] for args, kwargs in handle.write.call_args_list])