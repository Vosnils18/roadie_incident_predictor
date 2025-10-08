#!/usr/bin/env python3
"""
Example script demonstrating how to use the ANWB Road Events Predictor
for making incident probability predictions.
"""

import requests
import json
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000/api/predict/make_predictions/"
HEADERS = {"Content-Type": "application/json"}


def predict_incident_probability(
    temperature: float,
    rain_intensity: float,
    streetname: str,
    gforce: float,
    speed_limit: int,
    wind_speed: float,
    event_datetime: str
) -> dict:
    """
    Make a prediction request to the ANWB API.
    
    Args:
        temperature: Temperature in Celsius (-20 to 40)
        rain_intensity: Rainfall in mm/h (0 to 100)
        streetname: Road identifier (e.g., "A2", "N201")
        gforce: G-force measurement (0 to 10)
        speed_limit: Posted speed limit in km/h
        wind_speed: Wind speed in km/h (0 to 100)
        event_datetime: ISO format datetime string
    
    Returns:
        dict: Response containing prediction or error
    """
    payload = {
        "temp": temperature,
        "rain": rain_intensity,
        "streetname": streetname,
        "gforce": gforce,
        "speedlimit": speed_limit,
        "windspeed": wind_speed,
        "datetime": event_datetime
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def interpret_risk(prediction: float) -> str:
    """Interpret the prediction value into a risk level."""
    if prediction < 20:
        return "🟢 LOW - Normal conditions"
    elif prediction < 40:
        return "🟡 MODERATE - Slightly elevated risk"
    elif prediction < 60:
        return "🟠 HIGH - Significantly elevated risk"
    elif prediction < 80:
        return "🔴 VERY HIGH - Dangerous conditions"
    else:
        return "🚫 EXTREME - Critical conditions"


def example_1_sunny_day():
    """Example 1: Sunny day on highway A2"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Sunny Day on Highway A2")
    print("="*60)
    
    result = predict_incident_probability(
        temperature=22.0,
        rain_intensity=0.0,
        streetname="A2",
        gforce=5.0,
        speed_limit=100,
        wind_speed=8.0,
        event_datetime="2024-10-08T14:30:00"
    )
    
    if "prediction" in result:
        prediction = result["prediction"]
        print(f"Conditions: Sunny, 22°C, No rain, Light wind")
        print(f"Prediction: {prediction:.2f}")
        print(f"Risk Level: {interpret_risk(prediction)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def example_2_rainy_evening():
    """Example 2: Rainy evening with heavy traffic"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Rainy Evening Rush Hour")
    print("="*60)
    
    result = predict_incident_probability(
        temperature=12.0,
        rain_intensity=8.5,
        streetname="A4",
        gforce=6.2,
        speed_limit=120,
        wind_speed=25.0,
        event_datetime="2024-10-08T18:00:00"
    )
    
    if "prediction" in result:
        prediction = result["prediction"]
        print(f"Conditions: Rainy, 12°C, Heavy rain (8.5mm/h), Strong wind")
        print(f"Prediction: {prediction:.2f}")
        print(f"Risk Level: {interpret_risk(prediction)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def example_3_night_time():
    """Example 3: Clear night on provincial road"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Clear Night on Provincial Road")
    print("="*60)
    
    result = predict_incident_probability(
        temperature=8.0,
        rain_intensity=0.0,
        streetname="N201",
        gforce=4.5,
        speed_limit=80,
        wind_speed=5.0,
        event_datetime="2024-10-08T02:30:00"
    )
    
    if "prediction" in result:
        prediction = result["prediction"]
        print(f"Conditions: Clear night, 8°C, No rain, Calm wind")
        print(f"Prediction: {prediction:.2f}")
        print(f"Risk Level: {interpret_risk(prediction)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def example_4_storm():
    """Example 4: Stormy weather conditions"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Stormy Weather")
    print("="*60)
    
    result = predict_incident_probability(
        temperature=10.0,
        rain_intensity=25.0,
        streetname="A1",
        gforce=7.5,
        speed_limit=100,
        wind_speed=60.0,
        event_datetime="2024-10-08T11:00:00"
    )
    
    if "prediction" in result:
        prediction = result["prediction"]
        print(f"Conditions: Storm, 10°C, Very heavy rain (25mm/h), Gale force wind")
        print(f"Prediction: {prediction:.2f}")
        print(f"Risk Level: {interpret_risk(prediction)}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


def batch_prediction_example():
    """Example 5: Batch predictions for multiple roads"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Batch Predictions for Multiple Roads")
    print("="*60)
    
    roads = [
        {"name": "A2", "temp": 15, "rain": 2.0, "wind": 10},
        {"name": "A4", "temp": 14, "rain": 5.0, "wind": 15},
        {"name": "A1", "temp": 16, "rain": 1.0, "wind": 8},
        {"name": "N201", "temp": 13, "rain": 3.0, "wind": 12},
    ]
    
    predictions = []
    for road in roads:
        result = predict_incident_probability(
            temperature=road["temp"],
            rain_intensity=road["rain"],
            streetname=road["name"],
            gforce=5.0,
            speed_limit=100,
            wind_speed=road["wind"],
            event_datetime="2024-10-08T15:00:00"
        )
        
        if "prediction" in result:
            predictions.append({
                "road": road["name"],
                "prediction": result["prediction"]
            })
    
    # Sort by risk (highest first)
    predictions.sort(key=lambda x: x["prediction"], reverse=True)
    
    print("\nRoad Risk Rankings:")
    print("-" * 40)
    for i, pred in enumerate(predictions, 1):
        print(f"{i}. {pred['road']:8} - {pred['prediction']:6.2f} - {interpret_risk(pred['prediction'])}")


def check_api_health():
    """Check if the API is reachable"""
    try:
        # Make a simple test request
        result = predict_incident_probability(
            temperature=15.0,
            rain_intensity=0.0,
            streetname="A2",
            gforce=5.0,
            speed_limit=100,
            wind_speed=10.0,
            event_datetime=datetime.now().isoformat()
        )
        
        if "prediction" in result:
            print("✅ API is healthy and responding")
            return True
        else:
            print(f"⚠️  API returned error: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ API is not reachable: {str(e)}")
        print(f"\nMake sure the Django backend is running:")
        print(f"  cd backend")
        print(f"  python manage.py runserver")
        return False


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("ANWB Road Events Predictor - Usage Examples")
    print("="*60)
    
    # Check API health first
    if not check_api_health():
        return
    
    # Run examples
    example_1_sunny_day()
    example_2_rainy_evening()
    example_3_night_time()
    example_4_storm()
    batch_prediction_example()
    
    print("\n" + "="*60)
    print("Examples completed successfully!")
    print("="*60)
    print("\nNOTE: Predictions are probabilities, not certainties.")
    print("Always exercise caution when driving and consider local conditions.")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
