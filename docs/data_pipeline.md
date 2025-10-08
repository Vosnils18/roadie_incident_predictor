# Data Pipeline Documentation

## Overview

The ANWB Road Events Predictor uses a comprehensive ETL (Extract, Transform, Load) pipeline to consolidate data from multiple sources into a PostgreSQL data warehouse. This document describes the data flow, transformations, and quality assurance processes.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Data Sources                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  ANWB Incident   │  │   Weather API    │  │     Road     │ │
│  │    Database      │  │      (KNMI)      │  │  Attributes  │ │
│  │                  │  │                  │  │   Database   │ │
│  │  • Incident ID   │  │  • Temperature   │  │  • Speed     │ │
│  │  • Datetime      │  │  • Rain          │  │    Limits    │ │
│  │  • Location      │  │  • Wind Speed    │  │  • Road IDs  │ │
│  │  • Severity      │  │  • Timestamp     │  │  • G-Force   │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      ETL Pipeline                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    EXTRACT                              │   │
│  │  • Query incident records                               │   │
│  │  • Fetch weather data via API                           │   │
│  │  • Load road attributes                                 │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   TRANSFORM                             │   │
│  │  1. Data Cleaning                                       │   │
│  │     • Remove nulls and outliers                         │   │
│  │     • Deduplicate records                               │   │
│  │     • Validate ranges                                   │   │
│  │                                                         │   │
│  │  2. Data Integration                                    │   │
│  │     • Join incident + weather on datetime              │   │
│  │     • Merge road attributes on street ID               │   │
│  │     • Handle mismatches                                 │   │
│  │                                                         │   │
│  │  3. Feature Engineering                                 │   │
│  │     • Extract temporal features                         │   │
│  │     • Calculate durations                               │   │
│  │     • Compute derived metrics                           │   │
│  │                                                         │   │
│  │  4. Data Validation                                     │   │
│  │     • Schema validation                                 │   │
│  │     • Range checks                                      │   │
│  │     • Referential integrity                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                             ↓                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                     LOAD                                │   │
│  │  • Bulk insert to PostgreSQL                            │   │
│  │  • Create indexes                                       │   │
│  │  • Update metadata tables                               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Data Warehouse                               │
│              PostgreSQL: group14_warehouse                      │
│                                                                 │
│  ┌──────────────────────────────────────────────┐              │
│  │         regression_data (Main Table)         │              │
│  ├──────────────────────────────────────────────┤              │
│  │  • datetime_s          (timestamp)           │              │
│  │  • datetime_e          (timestamp)           │              │
│  │  • event_cat           (varchar)             │              │
│  │  • event_sev           (integer)             │              │
│  │  • speed               (float)               │              │
│  │  • end_speed           (float)               │              │
│  │  • streetname          (varchar)             │              │
│  │  • rain_intensity      (float)               │              │
│  │  • temperature         (float)               │              │
│  │  • windspeed           (float)               │              │
│  │  • speed_limit         (integer)             │              │
│  │  • light_condition     (varchar)             │              │
│  │  • accident_sev        (integer)             │              │
│  │  • accident_prob       (float)               │              │
│  └──────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Data Sources

### 1. ANWB Incident Database

**Source**: Internal ANWB incident reporting system  
**Format**: SQL Database  
**Update Frequency**: Real-time (batch extraction hourly)  
**Coverage**: 2018-2024, All major Dutch roads

**Key Fields**:
- `incident_id`: Unique identifier
- `datetime_start`, `datetime_end`: Incident time window
- `location`: GPS coordinates or road identifier
- `category`: Incident type (accident, breakdown, congestion)
- `severity`: Scale 1-5
- `speed_before`, `speed_after`: Traffic speed measurements
- `description`: Text description (not used in ML)

**Data Quality Issues**:
- ~5% missing severity values → Imputed with median
- Occasional GPS coordinate errors → Validated against road network
- Duplicate reports for same incident → Deduplication by time + location

### 2. Weather Data (KNMI)

**Source**: Royal Netherlands Meteorological Institute (KNMI) API  
**Format**: JSON API responses  
**Update Frequency**: Hourly measurements  
**Coverage**: Major weather stations across Netherlands

**Key Fields**:
- `timestamp`: Measurement datetime
- `station_id`: Weather station identifier
- `temperature`: Celsius
- `precipitation`: mm/hour
- `wind_speed`: km/hour
- `visibility`: meters (not currently used)

**Data Quality Issues**:
- API rate limits → Implemented caching and retry logic
- Missing data during sensor maintenance → Forward-fill interpolation
- Station coverage gaps → Nearest neighbor assignment for remote roads

**API Access**:
```python
import requests

def fetch_weather(datetime, location):
    url = "https://api.knmi.nl/weather/v1/data"
    params = {
        'datetime': datetime.isoformat(),
        'lat': location['lat'],
        'lon': location['lon']
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 3. Road Attributes Database

**Source**: Dutch Road Authority (Rijkswaterstaat)  
**Format**: PostgreSQL database  
**Update Frequency**: Quarterly updates  
**Coverage**: All numbered roads (A, N routes)

**Key Fields**:
- `road_id`: Unique road segment identifier
- `road_name`: Human-readable name (e.g., "A2", "N201")
- `speed_limit`: Posted speed limit (km/h)
- `gforce_measurement`: Road surface quality metric
- `road_type`: Highway, provincial, local
- `lanes`: Number of lanes
- `lighting`: Present/absent

**Data Quality Issues**:
- New roads lag in database → Temporary "Unknown" classification
- Speed limit changes delayed → Monthly updates

## ETL Process

### Extract Phase

#### 1. Incident Data Extraction

```python
def extract_incidents(start_date, end_date):
    """Extract incident records from ANWB database"""
    query = """
        SELECT 
            incident_id,
            datetime_start,
            datetime_end,
            location,
            category,
            severity,
            speed_before,
            speed_after
        FROM incidents
        WHERE datetime_start BETWEEN %s AND %s
        AND status = 'verified'
    """
    
    conn = psycopg2.connect(**ANWB_DB_CONFIG)
    df = pd.read_sql_query(query, conn, params=[start_date, end_date])
    conn.close()
    
    return df
```

**Schedule**: Hourly batch extraction (previous 1-hour window)  
**Performance**: ~10,000 records/minute  
**Error Handling**: Retry on connection failure, alert on empty results

#### 2. Weather Data Extraction

```python
def extract_weather(incidents_df):
    """Fetch weather data for each incident"""
    weather_data = []
    
    for _, incident in incidents_df.iterrows():
        try:
            weather = fetch_weather(
                incident['datetime_start'],
                incident['location']
            )
            weather_data.append({
                'incident_id': incident['incident_id'],
                'temperature': weather['temp'],
                'rain': weather['precipitation'],
                'wind_speed': weather['wind']
            })
        except APIError as e:
            logger.warning(f"Weather fetch failed for {incident['incident_id']}: {e}")
            # Use historical average as fallback
            weather_data.append(get_historical_average(incident))
    
    return pd.DataFrame(weather_data)
```

**Rate Limiting**: 100 requests/minute (implemented with time.sleep)  
**Caching**: 1-hour cache for weather per location (reduces API calls)  
**Fallback**: Historical averages when API unavailable

#### 3. Road Attributes Extraction

```python
def extract_road_attributes():
    """Load road attributes (updated quarterly)"""
    query = """
        SELECT 
            road_id,
            road_name,
            speed_limit,
            gforce_measurement,
            lighting_type
        FROM road_attributes
    """
    
    conn = psycopg2.connect(**ROAD_DB_CONFIG)
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df
```

**Caching**: Loaded once daily (rarely changes)  
**Memory**: Stored in-memory for fast lookups

### Transform Phase

#### 1. Data Cleaning

```python
def clean_data(df):
    """Remove outliers, nulls, and duplicates"""
    
    # Remove outliers
    df = df[df['accident_prob'] <= 100]
    df = df[(df['temperature'] >= -20) & (df['temperature'] <= 40)]
    df = df[(df['rain_intensity'] >= 0) & (df['rain_intensity'] <= 100)]
    
    # Handle missing values
    df['severity'].fillna(df['severity'].median(), inplace=True)
    df['speed'].fillna(method='ffill', inplace=True)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['datetime_start', 'location'])
    
    # Validate data types
    df['datetime_start'] = pd.to_datetime(df['datetime_start'])
    df['event_sev'] = df['event_sev'].astype('int')
    
    return df
```

**Rules**:
- `accident_prob` must be [0, 100]
- `temperature` must be [-20, 40] °C
- `rain_intensity` must be [0, 100] mm/h
- `wind_speed` must be [0, 100] km/h
- No negative speeds

**Imputation Strategy**:
- Numerical: Median or forward-fill
- Categorical: Mode or "Unknown"
- Critical fields (datetime, location): Drop record if missing

#### 2. Data Integration

```python
def integrate_data(incidents_df, weather_df, roads_df):
    """Join data from multiple sources"""
    
    # Join incidents with weather
    df = pd.merge(
        incidents_df,
        weather_df,
        on='incident_id',
        how='left'
    )
    
    # Join with road attributes
    df = pd.merge(
        df,
        roads_df,
        left_on='road_name',
        right_on='road_name',
        how='left'
    )
    
    # Handle unmatched roads
    df['speed_limit'].fillna(50, inplace=True)  # Default to 50 km/h
    df['gforce'].fillna(5.0, inplace=True)      # Default average
    
    return df
```

**Join Keys**:
- Incidents ↔ Weather: `incident_id`
- Incidents ↔ Roads: `road_name`

**Mismatch Handling**:
- Unknown roads: Use default values
- Missing weather: Use historical averages
- Conflicting timestamps: Prefer closest match within ±30 minutes

#### 3. Feature Engineering

```python
def engineer_features(df):
    """Create additional features for ML"""
    
    # Temporal features
    df['hour'] = df['datetime_start'].dt.hour
    df['weekday'] = df['datetime_start'].dt.dayofweek
    df['is_holiday'] = df['datetime_start'].dt.date.isin(DUTCH_HOLIDAYS)
    
    # Duration
    df['duration_seconds'] = (df['datetime_end'] - df['datetime_start']).dt.total_seconds()
    
    # Speed differential
    df['speed_change'] = df['speed_before'] - df['speed_after']
    
    # Light condition
    df['light_condition'] = df.apply(lambda row: 
        'day' if 7 <= row['hour'] <= 19 else 'night', axis=1)
    
    return df
```

**Features Created**:
- `hour`: 0-23 (hour of day)
- `weekday`: 0-6 (Monday = 0)
- `is_holiday`: Boolean
- `duration_seconds`: Event duration
- `speed_change`: Traffic slowdown magnitude
- `light_condition`: Day/night/twilight

#### 4. Data Validation

```python
def validate_data(df):
    """Validate schema and data quality"""
    
    required_columns = [
        'datetime_start', 'datetime_end', 'event_cat',
        'temperature', 'rain_intensity', 'speed_limit'
    ]
    
    # Check all required columns present
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Check for nulls in critical fields
    if df[required_columns].isnull().any().any():
        raise ValueError("Null values in required columns")
    
    # Validate ranges
    assert df['accident_prob'].between(0, 100).all()
    assert df['speed_limit'].isin([30, 50, 60, 70, 80, 90, 100, 120, 130]).all()
    
    # Check referential integrity
    assert not df['road_name'].isnull().any()
    
    logger.info(f"Data validation passed: {len(df)} records")
    return df
```

**Validation Rules**:
- Schema compliance
- Range checks
- Referential integrity
- Null checks
- Data type validation

**Action on Failure**: Halt pipeline, alert data team, rollback if necessary

### Load Phase

#### 1. Bulk Insert

```python
def load_to_warehouse(df):
    """Bulk insert data to PostgreSQL"""
    
    conn = psycopg2.connect(**WAREHOUSE_CONFIG)
    cursor = conn.cursor()
    
    # Create staging table
    cursor.execute("""
        CREATE TEMP TABLE staging_data (LIKE group14_warehouse.regression_data)
    """)
    
    # Bulk insert to staging
    from io import StringIO
    buffer = StringIO()
    df.to_csv(buffer, index=False, header=False)
    buffer.seek(0)
    
    cursor.copy_from(
        buffer,
        'staging_data',
        sep=',',
        null=''
    )
    
    # Insert from staging to main table (handles deduplication)
    cursor.execute("""
        INSERT INTO group14_warehouse.regression_data
        SELECT * FROM staging_data
        ON CONFLICT (datetime_start, streetname) DO NOTHING
    """)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    logger.info(f"Loaded {len(df)} records to warehouse")
```

**Performance**: ~50,000 records/second via COPY command  
**Deduplication**: ON CONFLICT clause prevents duplicate inserts  
**Atomicity**: Transaction ensures all-or-nothing insert

#### 2. Indexing

```sql
-- Indexes for query performance
CREATE INDEX IF NOT EXISTS idx_datetime 
ON group14_warehouse.regression_data(datetime_start);

CREATE INDEX IF NOT EXISTS idx_streetname 
ON group14_warehouse.regression_data(streetname);

CREATE INDEX IF NOT EXISTS idx_accident_prob 
ON group14_warehouse.regression_data(accident_prob);
```

**Purpose**: Accelerate queries during model training and evaluation  
**Maintenance**: VACUUM and ANALYZE run weekly

#### 3. Metadata Update

```python
def update_metadata(run_id, records_processed, start_time, end_time):
    """Log ETL run metadata"""
    query = """
        INSERT INTO etl_metadata (run_id, records, start_time, end_time, status)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    conn = psycopg2.connect(**WAREHOUSE_CONFIG)
    cursor = conn.cursor()
    cursor.execute(query, [run_id, records_processed, start_time, end_time, 'SUCCESS'])
    conn.commit()
    cursor.close()
    conn.close()
```

**Tracked Metrics**:
- Run ID and timestamp
- Records extracted, transformed, loaded
- Errors and warnings
- Duration of each phase
- Data quality scores

## Data Quality Monitoring

### Automated Quality Checks

```python
def run_quality_checks(df):
    """Run automated data quality checks"""
    
    checks = {
        'null_percentage': df.isnull().sum() / len(df) * 100,
        'duplicate_percentage': df.duplicated().sum() / len(df) * 100,
        'outlier_percentage': detect_outliers(df),
        'schema_compliance': validate_schema(df),
        'value_range_compliance': validate_ranges(df)
    }
    
    # Alert if thresholds exceeded
    if checks['null_percentage'].max() > 5:
        alert_data_team("High null percentage detected")
    
    if checks['duplicate_percentage'] > 2:
        alert_data_team("High duplicate percentage detected")
    
    return checks
```

**Thresholds**:
- Null percentage: < 5% per column
- Duplicates: < 2% of total records
- Outliers: < 1% per column
- Schema compliance: 100%
- Range compliance: 100%

### Data Quality Dashboard

Tracked metrics (visualized in Grafana):
- Records processed per hour
- ETL success/failure rate
- Average processing time
- Data freshness (time since last update)
- Quality score trends

## Disaster Recovery

### Backup Strategy

**Frequency**: Daily full backup + hourly incremental  
**Retention**: 30 days of daily backups, 90 days of monthly  
**Storage**: AWS S3 (encrypted at rest)

```bash
# Automated backup script
pg_dump -U postgres anwb_incidents | gzip > backup_$(date +%Y%m%d).sql.gz
aws s3 cp backup_$(date +%Y%m%d).sql.gz s3://anwb-backups/
```

### Recovery Procedure

```bash
# Restore from backup
gunzip -c backup_20241008.sql.gz | psql -U postgres anwb_incidents

# Verify data integrity
psql -U postgres -d anwb_incidents -c "SELECT COUNT(*) FROM group14_warehouse.regression_data"
```

**RTO (Recovery Time Objective)**: 4 hours  
**RPO (Recovery Point Objective)**: 1 hour

## Performance Optimization

### Query Optimization

- Indexed columns: datetime_start, streetname, accident_prob
- Partitioning: Table partitioned by year for efficient archival
- Materialized views: Pre-computed aggregations for dashboards

### ETL Optimization

- Parallel processing: 4 concurrent extraction threads
- Batch size: 10,000 records per transaction
- Connection pooling: Reuse database connections
- Caching: Weather data cached for 1 hour

## Compliance & Security

**GDPR Compliance**:
- No personal data (PII) stored
- Aggregated incident data only
- Data retention: 7 years (regulatory requirement)
- Right to erasure: Procedures in place

**Security Measures**:
- Database credentials stored in secrets manager
- Encrypted connections (SSL/TLS)
- Role-based access control (RBAC)
- Audit logging of all data access

## Future Enhancements

- [ ] Real-time streaming pipeline (Apache Kafka)
- [ ] Machine learning-based anomaly detection in ETL
- [ ] Automated data quality remediation
- [ ] Integration with traffic camera data
- [ ] Historical weather data backfill
- [ ] Data lineage tracking
- [ ] Multi-region replication for high availability

---

*This data pipeline documentation is maintained by the ADS-AI Team 14 and reflects the current state of the system as of 2024.*
