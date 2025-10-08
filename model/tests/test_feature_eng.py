import pytest

import pandas as pd
import numpy as np

from model.feature_eng import create_additional_datetime_features, calculate_gforce, set_speed_limit 

# Sample DataFrame for testing
@pytest.fixture
def sample_data():
    data = {
        'datetime_s': pd.to_datetime(['2023-05-04 08:00:00', '2023-04-01 14:00:00']),
        'datetime_e': pd.to_datetime(['2023-05-04 08:05:00', '2023-04-01 14:10:00']),
        'event_cat': [1, 3],
        'maxwaarde': [1.5, 60],
        'speed': [50, 50],
        'speed_limit': ['50', 'No'],
    }
    return pd.DataFrame(data)

def test_set_speed_limit(sample_data):
    df = set_speed_limit(sample_data)
    assert 'speed_limit' in df.columns
    assert df['speed_limit'].dtype == np.int64
    assert df.loc[1, 'speed_limit'] == 0

def test_create_additional_datetime_features(sample_data):
    df = create_additional_datetime_features(sample_data)
    assert 'is_holiday' in df.columns
    assert 'weekday' in df.columns
    assert 'hour' in df.columns
    assert 'duration_in_s' in df.columns
    assert df['is_holiday'].dtype == np.bool_
    assert df.loc[0, 'is_holiday'] == True
    assert df.loc[1, 'is_holiday'] == False

def test_calculate_gforce(sample_data):
    df = create_additional_datetime_features(sample_data)
    df['speed_limit'] = df['speed_limit'].replace("No", "0").astype(int)
    df = calculate_gforce(df)
    assert 'gforce' in df.columns
    assert df.loc[0, 'gforce'] is not None
    assert (df['gforce'] >= 0).all() and (df['gforce'] <= 2).all()

if __name__ == "__main__":
    pytest.main()
