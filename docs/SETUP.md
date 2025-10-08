# Setup and Installation Guide

This guide will walk you through setting up the ANWB Road Events Predictor project on your local machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Model Training](#model-training)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows 10/11
- **RAM**: Minimum 8GB (16GB recommended for training)
- **Disk Space**: At least 5GB free space
- **GPU**: Optional (speeds up neural network training)

### Software Requirements

1. **Python 3.10.12**
   ```bash
   python --version  # Should show 3.10.12
   ```
   
   If you need to install Python 3.10:
   - **macOS**: `brew install python@3.10`
   - **Ubuntu/Debian**: `sudo apt install python3.10`
   - **Windows**: Download from [python.org](https://www.python.org/downloads/)

2. **PostgreSQL 12+** (for data warehouse)
   ```bash
   psql --version  # Should show 12.0 or higher
   ```
   
   Installation:
   - **macOS**: `brew install postgresql`
   - **Ubuntu/Debian**: `sudo apt install postgresql postgresql-contrib`
   - **Windows**: Download from [postgresql.org](https://www.postgresql.org/download/)

3. **Node.js 16+** (for frontend)
   ```bash
   node --version  # Should show v16.0.0 or higher
   npm --version
   ```
   
   Installation:
   - **macOS**: `brew install node`
   - **Ubuntu/Debian**: 
     ```bash
     curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
     sudo apt-get install -y nodejs
     ```
   - **Windows**: Download from [nodejs.org](https://nodejs.org/)

4. **Poetry** (Python package manager)
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/anwb-road-events-predictor.git
cd anwb-road-events-predictor
```

### 2. Set Up Python Environment

#### Option A: Using Poetry (Recommended)

```bash
# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

#### Option B: Using pip and venv

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"
python -c "import xgboost; print(f'XGBoost {xgboost.__version__}')"
python -c "import django; print(f'Django {django.__version__}')"
```

Expected output:
```
TensorFlow 2.15.0
XGBoost 2.0.3
Django 5.0.6
```

## Database Setup

### 1. Create PostgreSQL Database

```bash
# Start PostgreSQL service (if not running)
# macOS:
brew services start postgresql
# Linux:
sudo systemctl start postgresql
# Windows: Use pgAdmin or services

# Create database
createdb anwb_incidents

# Or using psql:
psql -U postgres
CREATE DATABASE anwb_incidents;
\q
```

### 2. Configure Database Connection

Create a `db_config.json` file in the project root:

```json
{
  "dbname": "anwb_incidents",
  "user": "your_username",
  "password": "your_password",
  "host": "localhost",
  "port": "5432"
}
```

**Security Note**: Add `db_config.json` to `.gitignore` to avoid committing credentials.

### 3. Load Data into Warehouse

```bash
cd model/warehouse_creation

# Run warehouse creation scripts
python create_warehouse.py

# Verify data
psql -U your_username -d anwb_incidents
SELECT COUNT(*) FROM group14_warehouse.regression_data;
\q
```

## Model Training

### Option 1: Train Models from Scratch

#### Train XGBoost Model

```bash
cd model
python final_xgb_training.py
```

This will:
- Load data from PostgreSQL
- Preprocess and engineer features
- Perform hyperparameter tuning
- Train the model
- Save to `weights_files/final/final_xgboost.pkl`

Expected duration: 10-30 minutes (depending on hardware)

#### Train Neural Network

```bash
python final_nn_training.py
```

This will:
- Load and preprocess data
- Train deep neural network
- Apply early stopping
- Save to `weights_files/final/final_nn_model.h5`

Expected duration: 30-60 minutes (faster with GPU)

### Option 2: Download Pre-trained Models

If pre-trained models are available:

```bash
# Download from project release or shared drive
wget https://example.com/models/final_xgboost.pkl -O model/weights_files/final/final_xgboost.pkl
wget https://example.com/models/final_nn_model.h5 -O model/weights_files/final/final_nn_model.h5
wget https://example.com/models/classes_streetname.npy -O model/weights_files/classes_streetname.npy
```

## Running the Application

### 1. Start the Backend (Django)

```bash
cd backend

# Run database migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The API will be available at: `http://localhost:8000/api/`

Test the API:
```bash
curl http://localhost:8000/api/predict/make_predictions/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"temp":15.5,"rain":2.3,"streetname":"A2","gforce":5.4,"speedlimit":100,"windspeed":12.0,"datetime":"2024-10-08T14:30:00"}'
```

### 2. Start the Frontend (React)

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at: `http://localhost:3000`

### 3. Access the Application

1. **Frontend UI**: Open browser to `http://localhost:3000`
2. **API Endpoint**: `http://localhost:8000/api/predict/make_predictions/`
3. **Django Admin**: `http://localhost:8000/admin/` (if superuser created)

## Project Structure Overview

After setup, your directory should look like:

```
anwb-road-events-predictor/
├── model/
│   ├── weights_files/
│   │   ├── final/
│   │   │   ├── final_xgboost.pkl
│   │   │   └── final_nn_model.h5
│   │   └── classes_streetname.npy
│   └── ...
├── backend/
│   ├── db.sqlite3  (created after migrations)
│   └── ...
├── frontend/
│   ├── node_modules/  (created after npm install)
│   └── ...
└── db_config.json  (you created this)
```

## Troubleshooting

### Common Issues

#### 1. PostgreSQL Connection Error

**Error**: `psycopg2.OperationalError: could not connect to server`

**Solution**:
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list                # macOS

# Start if not running
sudo systemctl start postgresql   # Linux
brew services start postgresql    # macOS
```

#### 2. Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'tensorflow'`

**Solution**:
```bash
# Ensure virtual environment is activated
poetry shell  # or source venv/bin/activate

# Reinstall dependencies
poetry install  # or pip install -r requirements.txt
```

#### 3. Model File Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'weights_files/final_xgboost.pkl'`

**Solution**:
```bash
# Train the models
cd model
python final_xgb_training.py
python final_nn_training.py
```

#### 4. CORS Error in Frontend

**Error**: `Access to XMLHttpRequest blocked by CORS policy`

**Solution**:
In `backend/backend/settings.py`, ensure:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

#### 5. Port Already in Use

**Error**: `Error: That port is already in use.`

**Solution**:
```bash
# Find process using port 8000
lsof -ti:8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
python manage.py runserver 8001
```

#### 6. Out of Memory During Training

**Error**: `ResourceExhaustedError: OOM when allocating tensor`

**Solution**:
```python
# Reduce batch size in final_nn_training.py
batch_size = 32  # instead of 64

# Or use GPU if available
# TensorFlow will automatically use GPU if detected
```

### Getting Help

If you encounter issues not covered here:

1. **Check the logs**: Look in terminal output for detailed error messages
2. **GitHub Issues**: Search existing issues or create a new one
3. **Documentation**: Refer to the [Model Card](docs/model_card.md) and [Methodology](docs/methodology.md)

## Next Steps

After successful setup:

1. **Explore the Data**: Check out notebooks in `model/EDA/`
2. **Run Tests**: `pytest model/tests/`
3. **Read Documentation**: Review `docs/` for detailed technical information
4. **Experiment**: Try different model parameters in training scripts
5. **Contribute**: Make improvements and submit pull requests!

## Environment Variables (Optional)

For production deployment, consider using environment variables:

```bash
# Create .env file
touch .env

# Add configurations
echo "DATABASE_URL=postgresql://user:password@localhost:5432/anwb_incidents" >> .env
echo "DEBUG=False" >> .env
echo "SECRET_KEY=your-secret-key-here" >> .env
```

Install python-dotenv:
```bash
pip install python-dotenv
```

## Docker Support (Advanced)

For containerized deployment:

```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Stop services
docker-compose down
```

---

**Congratulations!** 🎉 Your ANWB Road Events Predictor is now set up and running!

For questions or issues, please refer to the [documentation](docs/) or open an issue on GitHub.
