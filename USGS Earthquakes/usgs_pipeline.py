import dlt
from dlt.sources.rest_api import rest_api_source
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename=r'D:\My\my study\Courses\DE Projects\DTC Final Project\USGS Earthquakes\logs\usgs_pipeline.log', filemode='a')
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
                    "data_selector": "features",  # Extract data from the 'features' key
                    "pagination": "single_page",  # No pagination needed for this endpoint                           
                },  # No pagination needed for this endpoint
                "write_disposition": "merge",  # Use 'merge' to update existing records based on the primary key
                "primary_key": "id",
            }
        ],
    }
    logging.info("REST API source configured successfully.")
    return rest_api_source(config)


if __name__ == "__main__":
    # Create the pipeline
    logging.info("Creating the DLT pipeline for USGS earthquake data.")
    pipeline = dlt.pipeline(
            pipeline_name="usgs_earthquake_pipeline",
            destination="snowflake",
            dataset_name="usgs_data"
        )
    
    # Run the pipeline
    logging.info("Starting pipeline...")
    try:
        # 1. تهيئة المصدر أولاً وحفظه في متغير
        my_source = usgs_earthquake_source()
        
        # 2. تحديد مستوى دمج الجداول على المصدر نفسه
        # استخدام 0 يضمن وضع كل البيانات (بما فيها المصفوفات) في جدول واحد فقط
        my_source.max_table_nesting = 0 
        
        # 3. تشغيل الـ pipeline باستخدام المصدر بعد تعديله
        load_info = pipeline.run(my_source)
        
        logging.info("Pipeline run completed successfully.")
        logging.info(f"Load information: {load_info}")
    except Exception as e:
        logging.error(f"Error running pipeline: {e}")
    