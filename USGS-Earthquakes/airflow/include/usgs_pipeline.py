import dlt
from dlt.sources.rest_api import rest_api_source
import logging

def usgs_earthquake_source():
    """
    DLT source for USGS earthquake data using rest_api_source
    """
    logging.info("Configuring the REST API source for USGS earthquake data.")
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
                    "data_selector": "features",
                },
                "write_disposition": "merge",
                "primary_key": "id",
            }
        ],
    }
    logging.info("REST API source configured successfully.")
    return rest_api_source(config)


def create_and_run_pipeline():
    # 1. إعدادات الـ Logging جوه الفانكشن عشان متعملش Timeout لـ Airflow
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='/usr/local/airflow/include/logs/usgs_pipeline.log', 
        filemode='a'
    )
    
    # 2. الـ Try / Except بتحضن خطوات التنفيذ الفعلي
    try:
        logging.info("Creating the DLT pipeline for USGS earthquake data.")
        pipeline = dlt.pipeline(
            pipeline_name="usgs_earthquake_pipeline",
            destination="snowflake",
            dataset_name="usgs_data"
        )
        
        logging.info("Starting pipeline...")
        my_source = usgs_earthquake_source()
        my_source.max_table_nesting = 0 
        
        load_info = pipeline.run(my_source)
        
        logging.info("Pipeline run completed successfully.")
        logging.info(f"Load information: {load_info}")
        
    except Exception as e:
        # لو حصل أي خطأ هيتكتب في اللوج وكمان هيطبع على الشاشة قدامك
        logging.error(f"An error occurred while creating or running the pipeline: {e}")
        print(f"\nCRITICAL ERROR FOUND: {e}\n")


if __name__ == "__main__":
    create_and_run_pipeline()