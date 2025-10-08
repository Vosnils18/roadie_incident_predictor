import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout
import matplotlib.pyplot as plt

def load_data():
    # Example dataframe creation for demonstration
    data = {
        'event_cat': ['A', 'B', 'A', 'C'],
        'event_sev': [1, 2, 3, 1],
        'speed': [30, 40, 50, 60],
        'end_speed': [25, 35, 45, 55],
        'streetname': ['Street1', 'Street2', 'Street3', 'Street4'],
        'lat': [40.7128, 34.0522, 41.8781, 29.7604],
        'lon': [-74.0060, -118.2437, -87.6298, -95.3698],
        'rain_intensity': [0, 1, 0, 1],
        'temperature': [70, 80, 65, 90],
        'windspeed': [5, 10, 15, 20],
        'speed_limit': [50, 60, 70, 80],
        'light_condition': ['Day', 'Night', 'Day', 'Night'],
        'accident_sev': [0, 1, 0, 1],
        'accident_prob': [0.1, 0.9, 0.2, 0.8],
        'is_holiday': [0, 1, 0, 1],
        'weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday'],
        'gforce': [0.1, 0.2, 0.3, 0.4],
        'hour': [12, 14, 16, 18],
        'duration_in_s': [100, 200, 300, 400]
    }
    df = pd.DataFrame(data)
    return df

def preprocess_data(df):
    features = ['event_cat', 'event_sev', 'speed', 'end_speed', 'streetname', 'lat', 'lon', 'rain_intensity', 
                'temperature', 'windspeed', 'speed_limit', 'light_condition', 'is_holiday', 'weekday', 
                'gforce', 'hour', 'duration_in_s']
    targets = ['accident_sev', 'accident_prob']
    
    X = df[features]
    y = df[targets]
    
    numeric_features = ['event_sev', 'speed', 'end_speed', 'lat', 'lon', 'rain_intensity', 
                        'temperature', 'windspeed', 'speed_limit', 'gforce', 'hour', 'duration_in_s']
    categorical_features = ['event_cat', 'streetname', 'light_condition', 'is_holiday', 'weekday']
    
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])
    
    X_preprocessed = preprocessor.fit_transform(X)
    return X_preprocessed, y

def build_model(input_dim):
    inputs = Input(shape=(input_dim,))
    
    # Hidden layers
    x = Dense(128, activation='relu')(inputs)
    x = Dropout(0.2)(x)  # Adding Dropout for regularization
    x = Dense(64, activation='relu')(x)
    x = Dropout(0.2)(x)
    x = Dense(32, activation='relu')(x)
    
    # Outputs
    accident_sev_output = Dense(1, name='accident_sev')(x)
    accident_prob_output = Dense(1, name='accident_prob', activation='sigmoid')(x)
    
    # Model
    model = Model(inputs=inputs, outputs=[accident_sev_output, accident_prob_output])
    model.compile(optimizer='adam', 
                  loss={'accident_sev': 'mse', 'accident_prob': 'binary_crossentropy'}, 
                  metrics={'accident_sev': 'mae', 'accident_prob': 'accuracy'})
    
    return model

def plot_training_history(history):
    # Plotting the training history
    plt.figure(figsize=(12, 5))

    # Plot loss
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Total Loss')
    plt.plot(history.history['val_loss'], label='Validation Total Loss')
    plt.plot(history.history['accident_sev_loss'], label='Accident Severity Loss')
    plt.plot(history.history['val_accident_sev_loss'], label='Validation Accident Severity Loss')
    plt.plot(history.history['accident_prob_loss'], label='Accident Probability Loss')
    plt.plot(history.history['val_accident_prob_loss'], label='Validation Accident Probability Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Loss Over Epochs')

    # Plot accuracy
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accident_prob_accuracy'], label='Accident Probability Accuracy')
    plt.plot(history.history['val_accident_prob_accuracy'], label='Validation Accident Probability Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Accuracy Over Epochs')

    plt.tight_layout()
    plt.show()

def train_and_evaluate_model(model, X_train, X_test, y_train, y_test):
    history = model.fit(X_train, [y_train['accident_sev'], y_train['accident_prob']], 
                        epochs=50, batch_size=32, validation_split=0.2)
    
    loss, sev_loss, prob_loss, sev_mae, prob_acc = model.evaluate(X_test, [y_test['accident_sev'], y_test['accident_prob']])
    
    print(f"Loss: {loss}")
    print(f"Accident Severity Loss: {sev_loss}")
    print(f"Accident Probability Loss: {prob_loss}")
    print(f"Accident Severity MAE: {sev_mae}")
    print(f"Accident Probability Accuracy: {prob_acc}")
    
    # Plotting the training history
    plot_training_history(history)

def main():
    df = load_data()
    X, y = preprocess_data(df)
    
    # Splitting the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = build_model(X_train.shape[1])
    
    train_and_evaluate_model(model, X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()

