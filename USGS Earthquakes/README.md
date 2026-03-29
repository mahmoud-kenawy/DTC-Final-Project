# USGS Earthquakes Pipeline

This pipeline extracts earthquake data from the USGS (United States Geological Survey) API and loads it into Snowflake.

## Data Source
- **API URL**: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson
- **Data**: All earthquakes from the past month
- **Format**: GeoJSON

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Snowflake credentials**:
   The credentials are already configured in `.dlt/secrets.toml`. Make sure the password is set correctly.

3. **Run the pipeline**:
   ```bash
   python usgs_pipeline.py
   ```

## Pipeline Details

### What it does:
- Fetches all earthquake data from the USGS API
- Extracts all features (earthquake events) from the response
- Flattens the nested JSON structure for easier querying
- Loads the data into Snowflake

### Data Schema:
The pipeline creates a table with the following fields:
- **id**: Unique earthquake identifier
- **magnitude**: Earthquake magnitude
- **place**: Location description
- **time**: Occurrence time (timestamp)
- **updated**: Last update time
- **longitude, latitude, depth**: Geographic coordinates
- **url**: Link to detailed information
- **tsunami**: Tsunami warning indicator
- **felt**: Number of reports
- **And many more fields...**

### Snowflake Destination:
- **Database**: `dlt_data`
- **Schema**: `usgs_data`
- **Table**: `earthquakes`
- **Write Disposition**: `replace` (data is replaced on each run)

## Notes
- The pipeline uses the `replace` write disposition, meaning it will replace all data on each run
- If you want to append data instead, change `write_disposition="replace"` to `write_disposition="append"` in the code
- The primary key is set to `id` to prevent duplicates when using append mode
