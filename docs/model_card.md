# Model Card: ANWB Road Events Predictor

## Model Details

### Basic Information

- **Model Name**: ANWB Road Events Predictor
- **Model Version**: 1.0
- **Model Type**: Regression (Incident Probability Prediction)
- **Model Date**: 2024
- **Organization**: Breda University of Applied Sciences - ADS-AI Program
- **Contact**: Team 14 - Block D FAI1

### Model Architecture

#### Neural Network Model
- **Framework**: TensorFlow 2.15.0
- **Architecture**: 
  - Input layer: 15 features
  - Hidden layers: Multiple dense layers with dropout regularization
  - Output layer: Single neuron (regression output)
  - Activation functions: ReLU for hidden layers, linear for output
- **Training Algorithm**: Adam optimizer with learning rate scheduling
- **Loss Function**: Mean Squared Error (MSE)
- **Regularization**: Dropout layers to prevent overfitting

#### XGBoost Model
- **Framework**: XGBoost 2.0.3
- **Algorithm**: Gradient Boosted Decision Trees
- **Objective**: reg:squarederror
- **Evaluation Metric**: RMSE (Root Mean Squared Error)
- **Hyperparameter Tuning**: RandomizedSearchCV with cross-validation
- **Key Parameters**:
  - Learning rate: Optimized via random search
  - Max depth: Tuned between 3-10
  - Subsample ratio: 0.5-1.0
  - Column sampling: 0.5-1.0
  - Number of estimators: 100-1000

## Intended Use

### Primary Use Cases

1. **Proactive Safety Warnings**: Predict high-risk road conditions to alert ANWB members
2. **Resource Allocation**: Optimize deployment of emergency services and road maintenance
3. **Risk Assessment**: Provide real-time incident probability for specific road segments
4. **Policy Planning**: Support data-driven decisions for traffic safety improvements

### Intended Users

- **ANWB Operations Team**: For incident response planning
- **Traffic Management Centers**: For real-time risk monitoring
- **Research Teams**: For traffic safety analysis
- **ANWB Mobile App**: For driver notifications (future deployment)

### Out-of-Scope Use Cases

❌ **Autonomous Vehicle Decision Making**: The model is advisory only, not suitable for automated driving systems  
❌ **Individual Driver Profiling**: No personal driver data or behavior prediction  
❌ **Insurance Risk Assessment**: Not designed for individual insurance pricing  
❌ **Legal Evidence**: Predictions should not be used as legal evidence in accident cases  
❌ **Real-Time Critical Systems**: Model latency and uncertainty unsuitable for split-second decisions  

For full model card, see: docs/model_card.md in the repository
