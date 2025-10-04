# Mobility - GBFS Data Collection, real-time availability, and historical analysis

## Target GBFS Systems
- 1st Iteration: Seattle Lime
- 2nd Iteration: All US Reporters
- 3rd Iteration: All Reporters

## Use Cases:
- Real Time Dashboard showing current available entities
- Heat map of low fuel areas and high concentration
- Historical view and collection of missing/non-recent reporters
- Outage detection

## Update Frequency:
- API endpoint polling: every 30s
- Retention Policy: 1 year

## Tech Stack
- Python
- PostgreSQL + TimescaleDB
- Docker/ Airflow