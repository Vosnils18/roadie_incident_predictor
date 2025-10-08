import pytest
from unittest.mock import patch, Mock, MagicMock

import numpy as np
import json
import pandas as pd
from io import StringIO
from sklearn.preprocessing import StandardScaler

from model.preprocessing import (
    connection_db,
    fetch_data,
    remove_outliers,
    fix_dtypes,
    remove_duplicates,
    create_xy,
    split_tvt,
    normalize_data,
    main
)

sample_data = """
datetime_s,datetime_e,event_cat,event_sev,speed,end_speed,maxwaarde,streetname,rain_intensity,temperature,windspeed,speed_limit,light_condition,accident_sev,accident_prob
2018-01-01 00:21:41.100,2018-01-01 00:21:43.500,HARSH CORNERING,HC1,30.577536,37.014910,0.854562,Doornboslaan,0.0,8.8,12.87,Un,Daylight,Material Damage Only,3.467174
2018-01-01 00:18:20.500,2018-01-01 00:18:28.500,SPEED,SP1,82.076546,82.076546,86.904580,Backer en Ruebweg,0.0,8.8,12.87,Un,Darkness,Material Damage Only,3.049560
2018-01-01 00:18:20.500,2018-01-01 00:18:28.500,SPEED,SP1,82.076546,82.076546,86.904580,Backer en Ruebweg,0.0,8.8,12.87,Un,Darkness,Material Damage Only,3.049560
"""

@pytest.fixture
def mock_db_config(tmp_path):
    db_config_path = tmp_path / "db_config.json"
    db_config_content = {
        "dbname": "test_db",
        "user": "test_user",
        "password": "test_password",
        "host": "localhost",
        "port": 5432
    }
    with open(db_config_path, "w") as f:
        json.dump(db_config_content, f)
    return db_config_path

@patch('psycopg2.connect')
def test_connection_db(mock_connect, mock_db_config):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    conn, cursor = connection_db(mock_db_config)
    mock_connect.assert_called_once()
    mock_conn.cursor.assert_called_once()
    assert conn == mock_conn
    assert cursor == mock_cursor

@patch('psycopg2.connect')
def test_fetch_data(mock_connect, mock_db_config):
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        ('2018-01-01 00:21:41.100', '2018-01-01 00:21:43.500', 'HARSH CORNERING', 'HC1', 30.577536, 37.014910, 0.854562, 'Doornboslaan', 0.0, 8.8, 12.87, 'Un', 'Daylight', 'Material Damage Only', 3.467174),
        ('2018-01-01 00:18:20.500', '2018-01-01 00:18:28.500', 'SPEED', 'SP1', 82.076546, 82.076546, 86.904580, 'Backer en Ruebweg', 0.0, 8.8, 12.87, 'Un', 'Darkness', 'Material Damage Only', 3.049560)
    ]

    conn, cursor = connection_db(mock_db_config)
    df = fetch_data(conn, cursor)
    assert not df.empty
    assert len(df) == 2
    assert 'datetime_s' in df.columns

def test_remove_outliers():
    df = pd.read_csv(StringIO(sample_data))
    df = remove_outliers(df)
    assert df['accident_prob'].max() <= 100

def test_fix_dtypes():
    df = pd.read_csv(StringIO(sample_data))
    df = fix_dtypes(df, ['event_cat', 'event_sev', 'streetname', 'light_condition', 'accident_sev'], ['datetime_s', 'datetime_e'])
    assert pd.api.types.is_datetime64_any_dtype(df['datetime_s'])
    assert pd.api.types.is_integer_dtype(df['event_cat'])

def test_remove_duplicates():
    # Call the function with the mock DataFrame
    df_processed = remove_duplicates(pd.read_csv(StringIO(sample_data)))
    # Check if duplicates are removed correctly
    assert not df_processed.duplicated().any()
    # Additional checks if needed
    assert len(df_processed) < len(pd.read_csv(StringIO(sample_data)))

def test_create_xy():
    df = pd.read_csv(StringIO(sample_data))
    X, y = create_xy(df)
    assert 'accident_prob' not in X.columns
    assert 'accident_sev' not in X.columns
    assert y.name == 'accident_prob'

@pytest.fixture
def mock_x_and_y():
    # Generate mock data (assuming X and y are NumPy arrays)
    X = np.random.rand(100, 10)  # 100 samples, 10 features
    y = np.random.rand(100)  # Corresponding target values

    return X, y

def test_split_tvt(mock_x_and_y, caplog):
    X, y = mock_x_and_y

    # Call the function
    X_train, X_val, X_test, y_train, y_val, y_test = split_tvt(X, y)

    # Check if the shapes are correct
    assert X_train.shape[0] == 71  # 72% of total data for training
    assert X_val.shape[0] == 9   # 8% of total data for validation
    assert X_test.shape[0] == 20   # 20% for testing
    
    assert y_train.shape[0] == 71   # 72% of total data for training
    assert y_val.shape[0] == 9   # 8% of total data for validation
    assert y_test.shape[0] == 20   # 20% for testing

    # Check if logger info messages are logged correctly
    assert "X_train shape:" in caplog.text
    assert "X_val shape:" in caplog.text
    assert "X_test shape:" in caplog.text
    

@pytest.fixture
def mock_data():
    # Generate mock data (assuming X_train, X_val, and X_test are NumPy arrays)
    X_train = np.random.rand(100, 10)  # 100 samples, 10 features
    X_val = np.random.rand(20, 10) if np.random.randint(0, 2) == 1 else None  # 20 samples, 10 features (or None)
    X_test = np.random.rand(20, 10) if np.random.randint(0, 2) == 1 else None  # 20 samples, 10 features (or None)

    return X_train, X_val, X_test

def test_normalize_data(mock_data):
    X_train, X_val, X_test = mock_data

    # Call the function
    X_train_norm, X_val_norm, X_test_norm, scaler = normalize_data(X_train, X_val, X_test)

    # Check if scaler is fitted
    assert isinstance(scaler, StandardScaler)
    assert scaler.mean_.shape[0] == X_train.shape[1]

    # Check if X_train_norm is correctly normalized
    assert np.allclose(np.mean(X_train_norm, axis=0), 0, atol=1)
    assert np.allclose(np.std(X_train_norm, axis=0), 1, atol=1)

    # Check if X_val_norm and X_test_norm are None or correctly normalized
    if X_val is not None:
        assert X_val_norm is not None
        assert X_val_norm.shape == X_val.shape
        assert np.allclose(np.mean(X_val_norm, axis=0), 0, atol=1)
        assert np.allclose(np.std(X_val_norm, axis=0), 1, atol=1)

    if X_test is not None:
        assert X_test_norm is not None
        assert X_test_norm.shape == X_test.shape
        assert np.allclose(np.mean(X_test_norm, axis=0), 0, atol=1)
        assert np.allclose(np.std(X_test_norm, axis=0), 1, atol=1)

    X_train_norm, X_val_norm, X_test_norm, scaler = normalize_data(X_train)

    assert isinstance(scaler, StandardScaler)
    assert scaler.mean_.shape[0] == X_train.shape[1]

    # Cleanup
    del scaler  # Ensure scaler is deleted after the test
    

if __name__ == "__main__":
    pytest.main()
