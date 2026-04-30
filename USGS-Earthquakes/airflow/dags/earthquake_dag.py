from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2026, 4, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'earthquake_dag',
    default_args=default_args,
    schedule='@hourly',
    catchup=False,
    description='Fetches USGS data and transforms it using DLT and dbt.'
) as dag:

    # Flow: Batch data to Snowflake via DLT
    dlt_historical_load = BashOperator(
        task_id='dlt_historical_load',
        bash_command='cd /usr/local/airflow/include/ && python usgs_pipeline.py',
    )

    # Task: Trigger dbt transformations
    dbt_build = BashOperator(
        task_id='dbt_build',
        bash_command='cd /usr/local/airflow/usgs_earthquake_dbt && dbt build --profiles-dir .',
    )

    # Execute Flow: Batch pipeline to Snowflake (with dbt transformations)
    dlt_historical_load >> dbt_build
