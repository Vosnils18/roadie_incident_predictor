# API Documentation

## Overview

The ANWB Road Events Predictor API is a RESTful service built with Django REST Framework that provides real-time incident probability predictions based on road conditions, weather, and temporal factors.

**Base URL**: `http://localhost:8000/api/`  
**Version**: 1.0  
**Authentication**: Not required (development mode)  

## Endpoints

### 1. Make Prediction

Predicts the probability of a traffic incident occurring given specific conditions.

**Endpoint**: `/predict/make_predictions/`  
**Method**: `POST`  
**Content-Type**: `application/json`

#### Request Body

```json
{
  "temp": 15.5,                    // Temperature in Celsius
  "rain": 2.3,                     // Rain intensity in mm/h
  "streetname": "A2",              // Road identifier (string)
  "gforce": 5.4,                   // G-force measurement (float)
  "speedlimit": 100,               // Speed limit in km/h (integer)
  "windspeed": 12.0,               // Wind speed in km/h (float)
  "datetime": "2024-10-08T14:30:00" // ISO 8601 datetime string
}
```

#### Request Parameters

| Parameter | Type | Required | Range | Description |
|-----------|------|----------|-------|-------------|
| `temp` | float | Yes | -20 to 40 | Ambient temperature in °C |
| `rain` | float | Yes | 0 to 100 | Rainfall intensity in mm/h |
| `streetname` | string | Yes | - | Road identifier (e.g., "A2", "N201") |
| `gforce` | float | Yes | 0 to 10 | Road surface quality metric |
| `speedlimit` | integer | Yes | 30 to 130 | Posted speed limit in km/h |
| `windspeed` | float | Yes | 0 to 100 | Wind speed in km/h |
| `datetime` | string | Yes | ISO 8601 | Event datetime in format `YYYY-MM-DDTHH:MM:SS` |

#### Response

**Success (200 OK)**:
```json
{
  "prediction": 23.7
}
```

| Field | Type | Description |
|-------|------|-------------|
| `prediction` | float | Predicted incident probability (0-100 scale) |

**Error (500 Internal Server Error)**:
```json
{
  "error": "Prediction failed"
}
```

**Error (400 Bad Request)**:
```json
{
  "error": "Invalid input parameters"
}
```

#### Example Requests

**cURL**:
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

**Python (requests)**:
```python
import requests
import json

url = "http://localhost:8000/api/predict/make_predictions/"
payload = {
    "temp": 15.5,
    "rain": 2.3,
    "streetname": "A2",
    "gforce": 5.4,
    "speedlimit": 100,
    "windspeed": 12.0,
    "datetime": "2024-10-08T14:30:00"
}

response = requests.post(url, json=payload)
result = response.json()

print(f"Predicted incident probability: {result['prediction']:.2f}%")
```

**JavaScript (fetch)**:
```javascript
const url = "http://localhost:8000/api/predict/make_predictions/";
const payload = {
  temp: 15.5,
  rain: 2.3,
  streetname: "A2",
  gforce: 5.4,
  speedlimit: 100,
  windspeed: 12.0,
  datetime: "2024-10-08T14:30:00"
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload)
})
  .then(response => response.json())
  .then(data => console.log('Prediction:', data.prediction))
  .catch(error => console.error('Error:', error));
```

## Error Handling

### Common Error Codes

| Status Code | Meaning | Possible Causes |
|-------------|---------|-----------------|
| 200 | Success | Request processed successfully |
| 400 | Bad Request | Invalid input parameters, missing required fields |
| 404 | Not Found | Invalid endpoint URL |
| 500 | Internal Server Error | Model prediction failed, server error |
| 503 | Service Unavailable | Model not loaded, database connection failed |

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Validation Errors

**Missing Required Field**:
```json
{
  "error": "Missing required field: temp"
}
```

**Invalid Data Type**:
```json
{
  "error": "Invalid type for 'speedlimit': expected integer"
}
```

**Out of Range Value**:
```json
{
  "error": "Temperature out of valid range (-20 to 40)"
}
```

**Invalid Street Name**:
```json
{
  "error": "Unknown street name: 'XYZ123'"
}
```

## Rate Limiting

**Current Status**: No rate limiting implemented (development mode)

**Production Recommendations**:
- 100 requests per minute per IP address
- 1000 requests per hour per API key
- Burst allowance: 20 requests within 10 seconds

## Data Validation

### Input Validation Rules

The API performs the following validations:

1. **Temperature**: Must be between -20°C and 40°C
2. **Rain Intensity**: Must be between 0 and 100 mm/h
3. **Wind Speed**: Must be between 0 and 100 km/h
4. **Speed Limit**: Must be one of [30, 50, 60, 70, 80, 90, 100, 120, 130] km/h
5. **G-force**: Must be between 0 and 10
6. **Datetime**: Must be valid ISO 8601 format
7. **Street Name**: Must exist in trained encoder classes

### Street Name Handling

If an unknown street name is provided:
- The API maps it to 'Unknown' category
- Prediction is returned with reduced confidence
- Warning may be logged (not returned to client)

## Model Information

### Model Version
- **Neural Network**: TensorFlow 2.15.0
- **Training Date**: 2024
- **Data Coverage**: 2018-2024 historical incidents

### Feature Processing

The API automatically engineers the following features from your input:

**Temporal Features**:
- `hour`: Extracted from datetime (0-23)
- `weekday`: Extracted from datetime (0=Monday, 6=Sunday)
- `is_holiday`: Boolean flag for Dutch national holidays

**Derived Features**:
- `duration_in_s`: Set to default value (10 seconds)
- `event_cat`, `event_sev`: Set to default values
- `speed`, `end_speed`: Set to default values
- `light_condition`: Inferred from hour (day/night)

You only need to provide the 7 primary inputs; the API handles all feature engineering.

## Response Interpretation

### Prediction Scale

The `prediction` value represents incident probability on a 0-100 scale:

| Range | Risk Level | Interpretation |
|-------|------------|----------------|
| 0-20 | Low | Normal conditions, low incident risk |
| 20-40 | Moderate | Slightly elevated risk, standard caution advised |
| 40-60 | High | Significantly elevated risk, extra caution recommended |
| 60-80 | Very High | Dangerous conditions, avoid non-essential travel |
| 80-100 | Extreme | Critical conditions, travel strongly discouraged |

### Usage Guidelines

⚠️ **Important Disclaimers**:

1. **Predictions are Probabilities**: Not certainties. A low prediction doesn't guarantee safety.
2. **Advisory Only**: Predictions should inform, not replace, human judgment.
3. **Local Conditions**: Model may not capture hyperlocal conditions (e.g., specific curve visibility).
4. **Complementary Tool**: Use alongside other safety information (traffic reports, driver awareness).

## CORS Configuration

**Current Development Setup**:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React frontend
    "http://localhost:8000",  # Django admin
]
```

**Production Setup**:
Replace with actual production domains.

## Authentication & Security

**Current Status**: No authentication required (development mode)

**Production Recommendations**:
1. **API Keys**: Require API key in request headers
2. **OAuth 2.0**: For third-party integrations
3. **HTTPS Only**: Enforce encrypted connections
4. **Input Sanitization**: Additional validation against injection attacks
5. **Rate Limiting**: Prevent abuse and DDoS

## Monitoring & Logging

### Logged Information

The API logs the following for each request:

- Timestamp
- Input parameters
- Prediction output
- Processing time
- Any errors/exceptions

**Log Format**:
```
[2024-10-08 14:30:15] INFO: Prediction request received
[2024-10-08 14:30:15] DEBUG: Input - temp:15.5, rain:2.3, street:A2
[2024-10-08 14:30:15] INFO: Prediction: 23.7 (processing time: 45ms)
```

### Health Check (Future)

```
GET /api/health/
```

**Response**:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true,
  "version": "1.0"
}
```

## Changelog

### Version 1.0 (2024)
- Initial API release
- Single prediction endpoint
- Neural network model serving
- Basic error handling

### Planned Features (v1.1)
- [ ] Batch prediction endpoint
- [ ] Confidence intervals
- [ ] Feature importance explanation
- [ ] Health check endpoint
- [ ] API key authentication
- [ ] Rate limiting

## Support

For API issues or questions:
- **GitHub Issues**: [Report a bug](https://github.com/yourusername/anwb-road-events-predictor/issues)
- **Email**: team14@adsai.nl (placeholder)

## License

This API is part of the ANWB Road Events Predictor project developed at Breda University of Applied Sciences.

---

*Last updated: October 2024*
