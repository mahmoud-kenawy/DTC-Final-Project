# USGS Earthquakes Data Engineering Project

This project implements an end-to-end data pipeline that extracts earthquake data from the USGS (United States Geological Survey) API, loads it into Snowflake using `dlt`, transforms it using dbt, and orchestrates the workflow using Apache Airflow.

## Project Structure
- **Root**: `dlt` pipeline code (`usgs_pipeline.py`) to extract and load data into Snowflake.
- **airflow/**: Dedicated Airflow environment (Dockerfile, DAGs, Tests) to orchestrate the ELT pipeline.
- **usgs_earthquake_dbt/**: dbt project for transforming the raw earthquake data in Snowflake into analytics-ready models.

## Data Source
- **API URL**: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson
- **Data**: All earthquakes from the past month
- **Format**: GeoJSON

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Credentials**:
   - Make sure your Snowflake credentials are configured in `.dlt/secrets.toml` for the ingestion pipeline.
   - Configure Airflow connections and dbt profiles properly to point to your Snowflake data warehouse.

3. **Run the dlt pipeline manually**:
   ```bash
   python usgs_pipeline.py
   ```

## Pipeline Details

### Ingestion (dlt)
- Fetches all earthquake data from the USGS API.
- Extracts all features (earthquake events) from the response.
- Flattens the nested JSON structure for easier querying (`max_table_nesting = 0`).
- Loads the data into Snowflake (`usgs_data` schema).

### Destination Configuration (Snowflake)
- **Database**: Your configured Snowflake DB (e.g., `dlt_data`)
- **Schema**: `usgs_data`
- **Table**: `earthquakes`
- **Write Disposition**: `merge` (uses `id` as the primary key to upsert records and avoid duplicates)

### Transformation (dbt)
The `usgs_earthquake_dbt` directory contains transformations that clean, structure, and model the raw JSON data extracted by dlt.

### Orchestration (Airflow)
The `airflow` directory contains the setup needed to schedule the execution of the `dlt` ingestion script and subsequent `dbt` models.
