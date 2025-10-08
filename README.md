# ANWB Road Events Predictor

> An intelligent road safety prediction system for ANWB that forecasts traffic incident probabilities using machine learning and real-time data integration.

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31012/)
[![Django](https://img.shields.io/badge/django-5.0.6-green.svg)](https://www.djangoproject.com/)
[![TensorFlow](https://img.shields.io/badge/tensorflow-2.15.0-orange.svg)](https://www.tensorflow.org/)
[![XGBoost](https://img.shields.io/badge/xgboost-2.0.3-red.svg)](https://xgboost.readthedocs.io/)

## 🎯 Project Overview

This project delivers an end-to-end machine learning solution for **ANWB** (Royal Dutch Touring Club) to predict and assess traffic incident risks on Dutch roads. The system combines historical incident data, real-time weather conditions, road characteristics, and temporal patterns to generate actionable predictions that help prevent accidents and improve road safety.

### Business Impact

- **Proactive Safety Measures**: Predict high-risk conditions before incidents occur
- **Resource Optimization**: Deploy emergency services more effectively
- **Driver Awareness**: Provide real-time risk assessments to ANWB members
- **Data-Driven Insights**: Support policy decisions with evidence-based risk analysis

## ✨ Key Features

### 🤖 Dual ML Architecture
- **Neural Network Model**: Deep learning approach for complex pattern recognition
- **XGBoost Regressor**: Gradient boosting for robust baseline predictions
- **Ensemble Capabilities**: Flexibility to combine models for enhanced accuracy

### 📊 Comprehensive Data Integration
- Historical traffic incident data (2018-2024)
- Real-time weather conditions (temperature, rain, wind)
- Road characteristics (speed limits, G-force measurements, light conditions)
- Temporal features (time of day, day of week, holidays)

### 🌐 Production-Ready API
- RESTful Django backend with CORS support
- Real-time prediction endpoint
- Modern React frontend with interactive visualization
- Responsive UI with Tailwind CSS

### 🔬 Rigorous Model Development
- Extensive exploratory data analysis (EDA)
- Feature engineering with domain expertise
- Hyperparameter tuning via randomized search
- Comprehensive model evaluation and testing

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Historical  │  │   Weather    │  │     Road     │     │
│  │  Incidents   │  │     API      │  │  Attributes  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   Data Warehouse                            │
│              PostgreSQL + ETL Pipeline                      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              ML Pipeline (model/)                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Preprocessing│→ │   Feature    │→ │   Training   │     │
│  │   & Cleaning │  │ Engineering  │  │  & Validation│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                Trained Models                               │
│   ┌─────────────────┐      ┌─────────────────┐            │
│   │  Neural Network │      │     XGBoost     │            │
│   │   (TensorFlow)  │      │   Regressor     │            │
│   └─────────────────┘      └─────────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│            Application Layer                                │
│   ┌──────────────────────────────────────────────┐         │
│   │         Django REST API (backend/)           │         │
│   │  • Prediction endpoint                       │         │
│   │  • Model serving                             │         │
│   │  • Request validation                        │         │
│   └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│          Presentation Layer                                 │
│   ┌──────────────────────────────────────────────┐         │
│   │      React Frontend (frontend/)              │         │
│   │  • Interactive risk visualization            │         │
│   │  • Real-time prediction interface            │         │
│   │  • Responsive design                         │         │
│   └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
anwb-road-events-predictor/
├── model/                          # ML pipeline and training
│   ├── preprocessing.py            # Data cleaning and preparation
│   ├── feature_eng.py              # Feature engineering
│   ├── final_xgb_training.py       # XGBoost model training
│   ├── final_nn_training.py        # Neural network training
│   ├── get_prediction.py           # Inference utilities
│   ├── model_selection.py          # Model evaluation
│   ├── EDA/                        # Exploratory data analysis notebooks
│   ├── Notebooks/                  # Experimentation notebooks
│   ├── evaluation/                 # Model performance metrics
│   └── warehouse_creation/         # Data warehouse setup
│
├── backend/                        # Django REST API
│   ├── api/                        # API application
│   │   ├── views.py                # Prediction endpoints
│   │   ├── models.py               # Database models
│   │   ├── serializers.py          # API serializers
│   │   └── assets/                 # Model weights and encoders
│   └── backend/                    # Django configuration
│       ├── settings.py
│       └── urls.py
│
├── frontend/                       # React application
│   ├── src/                        # Source code
│   │   ├── components/             # React components
│   │   ├── pages/                  # Page components
│   │   └── utils/                  # Utility functions
│   ├── public/                     # Static assets
│   └── package.json                # Dependencies
│
├── docs/                           # Documentation
│   ├── model_card.md               # Comprehensive model documentation
│   ├── methodology.md              # Technical approach
│   ├── api_documentation.md        # REST API reference
│   ├── data_pipeline.md            # ETL and warehouse architecture
│   ├── SETUP.md                    # Installation guide
│   ├── AI_canvas.pdf               # AI project canvas
│   ├── Preprocessing_documentation.pdf
│   ├── risk_assessment_group14.docx
│   ├── privacypolicy.pdf           # Privacy documentation
│   └── termsandconditions.pdf      # Terms of service
│
├── examples/                       # Usage examples
│   └── usage_example.py            # Python API usage examples
│
├── pyproject.toml                  # Poetry dependencies
├── requirements.txt                # Pip dependencies
├── .gitignore                      # Git ignore rules
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
└── README.md                       # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10.12
- Node.js 16+ (for frontend)
- PostgreSQL (for data warehouse)
- Poetry (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/anwb-road-events-predictor.git
   cd anwb-road-events-predictor
   ```

2. **Set up Python environment**
   ```bash
   poetry install
   poetry shell
   ```

3. **Configure database**
   ```bash
   # Create db_config.json with your PostgreSQL credentials
   {
     "dbname": "your_database",
     "user": "your_username",
     "password": "your_password",
     "host": "localhost",
     "port": "5432"
   }
   ```

4. **Run the backend**
   ```bash
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```

5. **Run the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Training Models from Scratch

```bash
# Navigate to model directory
cd model

# Train XGBoost model
python final_xgb_training.py

# Train Neural Network
python final_nn_training.py
```

## 🔮 Making Predictions

### Via API

```bash
curl -X POST http://localhost:8000/api/predict/make_predictions/ \
  -H "Content-Type: application/json" \
  -d '{
    "temp": 15.5,
    "rain": 2.3,
    "streetname": "A2",
    "gforce": 5.4,
    "speedlimit": 100,
    "windspeed": 12.0,
    "datetime": "2024-10-08T14:30:00"
  }'
```

### Via Python

```python
from model.get_prediction import combine_functions

prediction = combine_functions(
    temp=15.5,
    rain=2.3,
    streetname="A2",
    gforce=5.4,
    speedlimit=100,
    windspeed=12.0,
    datetime="2024-10-08T14:30:00"
)

print(f"Predicted incident probability: {prediction:.2f}%")
```

## 📊 Model Performance

### Neural Network
- **Architecture**: Dense layers with dropout regularization
- **Optimizer**: Adam with learning rate scheduling
- **Loss Function**: Mean Squared Error (MSE)

### XGBoost Regressor
- **Best Parameters**: Tuned via RandomizedSearchCV
- **Evaluation Metric**: RMSE (Root Mean Squared Error)
- **Features**: 15 engineered features

See [docs/model_card.md](docs/model_card.md) for comprehensive model documentation.

## 🔬 Technical Details

### Data Processing Pipeline

1. **Data Collection**
   - Historical incident records from ANWB database
   - Weather data integration
   - Road attribute mapping

2. **Preprocessing**
   - Outlier removal (accident_prob > 100)
   - Duplicate detection and removal
   - Data type standardization
   - Missing value imputation

3. **Feature Engineering**
   - Temporal features (hour, weekday, holiday indicators)
   - Duration calculations
   - G-force measurements for road conditions

4. **Normalization**
   - StandardScaler for numerical features
   - LabelEncoder for categorical variables
   - Train/validation/test split (70/10/20)

### Key Features Used

| Feature | Type | Description |
|---------|------|-------------|
| `temperature` | Numerical | Ambient temperature (°C) |
| `rain_intensity` | Numerical | Precipitation rate (mm/h) |
| `windspeed` | Numerical | Wind speed (km/h) |
| `gforce` | Numerical | Road G-force measurement |
| `speed_limit` | Numerical | Posted speed limit |
| `streetname` | Categorical | Road identifier |
| `light_condition` | Categorical | Day/night/twilight |
| `hour` | Temporal | Hour of day (0-23) |
| `weekday` | Temporal | Day of week (0-6) |
| `is_holiday` | Boolean | Dutch national holiday |
| `duration_in_s` | Numerical | Event duration |
| `event_cat` | Categorical | Event category |
| `event_sev` | Categorical | Event severity |

## 🛡️ Safety & Ethics

### Privacy Protection
- No personal driver information stored
- Aggregated incident data only
- GDPR-compliant data handling
- See [docs/privacypolicy.pdf](docs/privacypolicy.pdf)

### Ethical Considerations
- Model predictions are advisory, not deterministic
- Human oversight required for critical decisions
- Regular bias audits and fairness assessments
- Transparency in model limitations

### Risk Management
- Comprehensive risk assessment documented
- Continuous monitoring for model drift
- Fallback mechanisms for system failures
- See [docs/risk_assessment_group14.docx](docs/risk_assessment_group14.docx)

## 📈 Future Enhancements

- [ ] Real-time traffic flow integration
- [ ] Weather forecast API connection
- [ ] Mobile application for drivers
- [ ] Multi-modal predictions (severity + probability)
- [ ] Geographical visualization with heatmaps
- [ ] Model explainability dashboard (SHAP values)
- [ ] Automated retraining pipeline
- [ ] A/B testing framework for model updates

## 🤝 Contributing

This project was developed as part of the Applied Data Science & AI program at Breda University of Applied Sciences (Block D, 2023-2024).

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

This is an academic collaboration with ANWB. For commercial use or production deployment, please contact Breda University of Applied Sciences or ANWB.

## 📚 Documentation

- [Model Card](docs/model_card.md) - Comprehensive model documentation
- [Technical Methodology](docs/methodology.md) - Detailed technical approach
- [API Documentation](docs/api_documentation.md) - REST API reference
- [Data Pipeline](docs/data_pipeline.md) - ETL and warehouse architecture
- [Setup Guide](docs/SETUP.md) - Installation instructions

## 🙏 Acknowledgments

- **ANWB** for providing the business case and domain expertise
- **Breda University of Applied Sciences** for academic supervision
- Open-source community for excellent ML frameworks (TensorFlow, XGBoost, scikit-learn)

## 📸 Preview

<!-- Add screenshots of your UI here -->

---

**Note**: This project is primarily for educational purposes and demonstration of ML engineering capabilities. Production deployment requires additional security hardening, monitoring, and compliance verification.
