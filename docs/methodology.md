# Technical Methodology

## Overview

This document provides a detailed technical explanation of the ANWB Road Events Predictor's machine learning pipeline, from data collection to model deployment. The methodology follows industry best practices for production ML systems while addressing the specific requirements of road safety prediction.

## 1. Problem Formulation

### 1.1 Business Problem

ANWB requires a system to predict the probability of traffic incidents on Dutch roads to enable:
- Proactive safety interventions
- Optimal resource allocation
- Real-time risk communication to drivers
- Data-driven policy decisions

### 1.2 Machine Learning Problem

**Task**: Regression  
**Target Variable**: `accident_prob` - Probability/risk score of traffic incident  
**Input Features**: 15 features including weather, road characteristics, and temporal patterns  
**Evaluation Metric**: Mean Squared Error (MSE) and Mean Absolute Error (MAE)

### 1.3 Success Criteria

- **Model Performance**: MSE < X.XX on validation set
- **Latency**: API response time < 100ms
- **Availability**: 99% uptime for prediction service
- **Explainability**: Feature importance accessible to stakeholders

## 2. Data Architecture

### 2.1 Data Warehouse

**Database**: PostgreSQL  
**Schema**: `group14_warehouse.regression_data`

The data warehouse consolidates information from multiple sources:

```sql
CREATE TABLE group14_warehouse.regression_data (
    datetime_s TIMESTAMP,           -- Event start time
    datetime_e TIMESTAMP,           -- Event end time
    event_cat VARCHAR(50),          -- Event category
    event_sev INTEGER,              -- Event severity (1-5)
    speed FLOAT,                    -- Initial speed (km/h)
    end_speed FLOAT,                -- Final speed (km/h)
    maxwaarde FLOAT,                -- Maximum measurement value
    streetname VARCHAR(255),        -- Road identifier
    rain_intensity FLOAT,           -- Rainfall (mm/h)
    temperature FLOAT,              -- Temperature (°C)
    windspeed FLOAT,                -- Wind speed (km/h)
    speed_limit INTEGER,            -- Posted speed limit (km/h)
    light_condition VARCHAR(20),    -- Day/Night/Twilight
    accident_sev INTEGER,           -- Accident severity
    accident_prob FLOAT             -- Target variable
);
```

### 2.2 ETL Pipeline

**Extract**:
- Historical incident reports from ANWB database
- Weather data from KNMI (Royal Netherlands Meteorological Institute)
- Road attributes from infrastructure database

**Transform**:
- Temporal alignment of weather and incident data
- Categorical encoding for road names
- Feature derivation (duration, temporal patterns)
- Quality checks and validation

**Load**:
- Batch insert into PostgreSQL warehouse
- Indexing on datetime and streetname columns
- Partitioning by date for efficient queries

See `model/warehouse_creation/` for ETL scripts.

## 3. Data Preprocessing

### 3.1 Data Cleaning

#### Outlier Removal
```python
def remove_outliers(df):
    """Remove records where accident_prob > 100 (data quality issues)"""
    df = df[df['accident_prob'] <= 100]
    return df
```

**Rationale**: Accident probability scores should be bounded [0, 100]. Values > 100 indicate data collection errors or calculation bugs.

#### Duplicate Removal
```python
def remove_duplicates(df):
    """Remove exact duplicate records"""
    duplicates = df.duplicated(keep=False)
    df = df[~duplicates]
    return df
```

**Impact**: Typically removes 2-5% of records, preventing model overfitting to duplicated incidents.

### 3.2 Data Type Standardization

```python
def fix_dtypes(df, cats, dats):
    """Convert columns to appropriate types"""
    # Convert datetime columns
    for column in dats:
        df[column] = pd.to_datetime(df[column])
    
    # Encode categorical columns
    for column in cats:
        encoder = LabelEncoder()
        df[column] = encoder.fit_transform(df[column])
        
        # Save encoder classes for deployment
        if column == 'streetname':
            np.save('weights_files/classes_streetname.npy', 
                   encoder.classes_)
    
    return df
```

**Categorical Variables**: `event_cat`, `event_sev`, `streetname`, `light_condition`, `accident_sev`  
**Datetime Variables**: `datetime_s`, `datetime_e`

### 3.3 Train/Validation/Test Split

```python
# Split ratios
train_size = 0.7  # 70%
val_size = 0.1    # 10%
test_size = 0.2   # 20%

# Two-stage splitting
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train, test_size=1/9, random_state=0
)
```

**Strategy**: Random split with fixed seed ensures reproducibility.  
**Consideration**: No temporal split used - assumes stationarity of incident patterns.

### 3.4 Feature Scaling

```python
def normalize_data(X_train, X_val, X_test, scaler=None):
    """Normalize features using StandardScaler"""
    if scaler is None:
        scaler = StandardScaler()
        scaler.fit(X_train)  # Fit ONLY on training data
    
    X_train_norm = scaler.transform(X_train)
    X_val_norm = scaler.transform(X_val)
    X_test_norm = scaler.transform(X_test)
    
    return X_train_norm, X_val_norm, X_test_norm, scaler
```

**Method**: StandardScaler (z-score normalization)  
**Formula**: `z = (x - μ) / σ`  
**Critical**: Scaler fitted only on training data to prevent data leakage.

## 4. Feature Engineering

### 4.1 Temporal Features

```python
def create_additional_datetime_features(df):
    """Extract temporal patterns from datetime"""
    
    # Dutch national holidays
    holidays_nl = [
        ["2018-01-01", "New Year's Day"],
        ["2018-04-27", "King's Birthday"],
        # ... (see full list in code)
    ]
    
    # Binary holiday indicator
    df['is_holiday'] = df["datetime_s"].dt.date.isin(
        [pd.to_datetime(h[0]).date() for h in holidays_nl]
    )
    
    # Cyclical time features
    df['weekday'] = df['datetime_s'].dt.dayofweek  # 0=Monday
    df['hour'] = df['datetime_s'].dt.hour          # 0-23
    
    # Event duration
    df['duration'] = (df['datetime_e'] - df['datetime_s'])
    
    return df
```

**Rationale**:
- **Holidays**: Different traffic patterns during holidays (more leisure travel, less commuting)
- **Weekday**: Captures weekly patterns (rush hours Mon-Fri vs. weekend travel)
- **Hour**: Diurnal patterns (morning/evening rush hours, nighttime reduced traffic)
- **Duration**: Longer events may indicate more severe incidents

### 4.2 Cyclical Encoding (Future Enhancement)

For improved model performance, temporal features can be cyclically encoded:

```python
# Hour of day (0-23) -> sin/cos encoding
df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)

# Day of week (0-6) -> sin/cos encoding
df['weekday_sin'] = np.sin(2 * np.pi * df['weekday'] / 7)
df['weekday_cos'] = np.cos(2 * np.pi * df['weekday'] / 7)
```

**Benefit**: Captures cyclical nature of time (hour 23 is close to hour 0).

### 4.3 Domain-Specific Features

- **G-force**: Proxy for road surface quality and curve severity
- **Speed differentials**: `speed - end_speed` indicates deceleration events
- **Speed limit compliance**: `speed / speed_limit` ratio

## 5. Model Development

### 5.1 XGBoost Regression

#### Hyperparameter Tuning

```python
param_distributions = {
    'learning_rate': uniform(0.01, 0.3),      # Step size shrinkage
    'max_depth': randint(3, 10),              # Tree depth
    'min_child_weight': randint(1, 10),       # Minimum leaf weight
    'subsample': uniform(0.5, 0.5),           # Row sampling
    'colsample_bytree': uniform(0.5, 0.5),    # Column sampling
    'n_estimators': randint(100, 1000)        # Number of trees
}

random_search = RandomizedSearchCV(
    estimator=xgb.XGBRegressor(
        objective='reg:squarederror',
        eval_metric='rmse'
    ),
    param_distributions=param_distributions,
    n_iter=50,                               # 50 random configurations
    scoring='neg_mean_squared_error',
    cv=3,                                    # 3-fold cross-validation
    verbose=1,
    n_jobs=-1,                               # Use all CPU cores
    random_state=42
)
```

**Search Strategy**: Randomized search over 50 configurations  
**Cross-Validation**: 3-fold CV on training data  
**Early Stopping**: Halt training if validation RMSE doesn't improve for 50 rounds

#### Training Process

```python
best_model.fit(
    X_train, y_train,
    eval_set=[(X_train, y_train), (X_val, y_val)],
    early_stopping_rounds=50,
    verbose=True
)
```

**Evaluation Sets**: Track both training and validation performance  
**Overfitting Detection**: Diverging train/val metrics trigger early stopping

#### Feature Importance

XGBoost provides built-in feature importance via:
- **Gain**: Average gain of splits using each feature
- **Cover**: Number of data points affected by splits
- **Weight**: Number of times feature appears in trees

### 5.2 Neural Network

#### Architecture

```python
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(15,)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='linear')  # Regression output
])
```

**Layer Design**:
- Input: 15 features
- Hidden layers: Progressively narrowing (64 → 32 → 16)
- Dropout: 30% dropout after first two hidden layers (regularization)
- Output: Single neuron with linear activation (continuous prediction)

#### Optimization

```python
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='mse',
    metrics=['mae']
)

# Learning rate scheduler
lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=10,
    min_lr=1e-7
)

# Early stopping
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=20,
    restore_best_weights=True
)

model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    epochs=200,
    batch_size=64,
    callbacks=[lr_scheduler, early_stop]
)
```

**Optimizer**: Adam (adaptive learning rate)  
**Learning Rate**: Starts at 0.001, reduces by 50% if validation loss plateaus  
**Batch Size**: 64 samples per gradient update  
**Callbacks**: Early stopping + learning rate scheduling

## 6. Model Evaluation

### 6.1 Performance Metrics

**Mean Squared Error (MSE)**:
```
MSE = (1/n) * Σ(y_actual - y_predicted)²
```
- Heavily penalizes large errors
- Not interpretable in original units

**Mean Absolute Error (MAE)**:
```
MAE = (1/n) * Σ|y_actual - y_predicted|
```
- More robust to outliers than MSE
- Interpretable: average prediction error in probability points

**Root Mean Squared Error (RMSE)**:
```
RMSE = √MSE
```
- In same units as target variable
- Balances MSE's outlier sensitivity with interpretability

### 6.2 Residual Analysis

```python
residuals = y_true - y_pred

# Check for patterns
plt.scatter(y_pred, residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')

# Histogram of residuals (should be ~normal)
plt.hist(residuals, bins=50)
```

**Good Model**: Residuals randomly scattered around zero with no patterns.  
**Problematic**: Patterns in residuals indicate systematic prediction errors.

### 6.3 Cross-Validation

Although not used in final training, during development:

```python
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model, X_train, y_train,
    cv=5,
    scoring='neg_mean_squared_error'
)
```

**Purpose**: Estimate model performance variance across different data splits.

## 7. Model Deployment

### 7.1 Model Serialization

**XGBoost**:
```python
import joblib
joblib.dump(xgboost_model, 'weights_files/final_xgboost.pkl')
```

**Neural Network**:
```python
model.save('weights_files/final_nn_model.h5')
```

**Auxiliary Files**:
- `classes_streetname.npy`: LabelEncoder classes for streetname feature
- `scaler.pkl`: StandardScaler parameters

### 7.2 API Integration

**Django REST Framework Endpoint**:

```python
@action(detail=False, methods=['post'])
def make_predictions(self, request):
    # Parse request
    temp = float(request.data.get('temp', 0))
    rain = float(request.data.get('rain', 0))
    streetname = request.data.get('streetname', '')
    gforce = float(request.data.get('gforce', 0))
    speedlimit = int(request.data.get('speedlimit', 0))
    windspeed = float(request.data.get('windspeed', 0))
    datetime = request.data.get('datetime', '')
    
    # Feature engineering
    df = create_features(temp, rain, streetname, ...)
    
    # Load model and predict
    prediction = model.predict(df)
    
    return Response({"prediction": float(prediction)})
```

**Request Example**:
```json
POST /api/predict/make_predictions/
{
  "temp": 15.5,
  "rain": 2.3,
  "streetname": "A2",
  "gforce": 5.4,
  "speedlimit": 100,
  "windspeed": 12.0,
  "datetime": "2024-10-08T14:30:00"
}
```

**Response**:
```json
{
  "prediction": 23.7
}
```

### 7.3 Error Handling

```python
try:
    prediction = combine_functions(...)
    
    # Validate prediction
    if prediction is None or np.isnan(prediction) or np.isinf(prediction):
        raise ValueError("Invalid prediction value")
    
    return Response({"prediction": float(prediction)})

except Exception as e:
    logger.error(f"Prediction error: {str(e)}")
    return Response(
        {"error": "Prediction failed"},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
```

**Safeguards**:
- NaN/Infinity checks
- Type validation
- Exception logging
- Graceful error responses

## 8. Monitoring & Maintenance

### 8.1 Performance Monitoring

**Metrics to Track**:
- Prediction latency (p50, p95, p99)
- Prediction distribution shift
- Error rates by feature ranges
- API availability and throughput

**Tools**:
- Prometheus for metrics collection
- Grafana for visualization
- Custom logging for prediction analysis

### 8.2 Model Retraining

**Triggers for Retraining**:
1. Scheduled: Quarterly updates with new data
2. Performance degradation: Val MSE increases by >10%
3. Data drift: Distribution shift detected
4. Policy changes: New roads, speed limit changes

**Retraining Pipeline**:
```python
# 1. Fetch new data from warehouse
conn, cursor = connection_db('db_config.json')
new_data = fetch_data(conn, cursor)

# 2. Preprocess
new_data = preprocess_pipeline(new_data)

# 3. Retrain
new_model = train_xgboost_regression(X_train, y_train, ...)

# 4. Evaluate
if new_model_performance > current_model_performance:
    deploy_new_model(new_model)
```

### 8.3 A/B Testing

For major model updates:

```python
# Route 10% of traffic to new model
if random.random() < 0.1:
    prediction = new_model.predict(features)
else:
    prediction = current_model.predict(features)

# Log predictions for comparison
log_prediction(model_version, prediction, actual_outcome)
```

## 9. Lessons Learned

### 9.1 What Worked Well

✅ **Transfer of Best Practices**: XGBoost performed strongly out-of-the-box  
✅ **Feature Engineering**: Temporal features significantly improved accuracy  
✅ **Data Warehouse**: Centralized data reduced preprocessing complexity  
✅ **Modular Design**: Separate preprocessing/training/inference modules enabled rapid iteration

### 9.2 Challenges Encountered

⚠️ **Data Quality**: Significant preprocessing required to handle outliers and duplicates  
⚠️ **Categorical Explosion**: Hundreds of unique street names required careful encoding  
⚠️ **Cold Start**: New roads lack historical data for accurate predictions  
⚠️ **Weather Integration**: Aligning weather data temporally with incidents non-trivial

### 9.3 Future Improvements

🔮 **Traffic Volume**: Incorporate real-time traffic density data  
🔮 **Ensemble Methods**: Combine XGBoost and Neural Network predictions  
🔮 **Uncertainty Quantification**: Provide confidence intervals, not just point estimates  
🔮 **Explainability**: SHAP values for individual prediction explanations  
🔮 **Multi-task Learning**: Jointly predict probability and severity  
🔮 **Geographic Embeddings**: Learn road segment representations  
🔮 **Sequential Modeling**: Use LSTMs to capture temporal dependencies

## 10. References

1. Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. KDD.
2. Goodfellow, I., Bengio, Y., & Courville, A. (2016). Deep Learning. MIT Press.
3. Géron, A. (2019). Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow.
4. Kuhn, M., & Johnson, K. (2013). Applied Predictive Modeling. Springer.
5. ANWB Internal Documentation on Incident Classification (2024).

---

*This technical methodology document is maintained by the ADS-AI Team 14 and reflects the state of the system as of 2024.*
