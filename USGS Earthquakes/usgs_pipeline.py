import dlt
from dlt.sources.rest_api import rest_api_source


def usgs_earthquake_source():
    """
    DLT source for USGS earthquake data using rest_api_source
    """
    # Configure the REST API source
    config = {
        "client": {
            "base_url": "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/",
        },
        "resources": [
            {
                "name": "earthquakes",
                "endpoint": {
                    "path": "all_month.geojson",
                    "data_selector": "features",  # Extract data from the 'features' key
                },
                "write_disposition": "replace",  # Replace data on each run
                "primary_key": "id",
            }
        ],
    }
    
    return rest_api_source(config)


if __name__ == "__main__":
    # Create the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="usgs_earthquakes_pipeline",
        destination="snowflake",
        dataset_name="usgs_data"
    )
    
    # Run the pipeline
    print("Starting pipeline...")
    load_info = pipeline.run(usgs_earthquake_source())
    
    # Print load information
    print(f"\nPipeline completed successfully!")
    print(f"Load info: {load_info}")
    