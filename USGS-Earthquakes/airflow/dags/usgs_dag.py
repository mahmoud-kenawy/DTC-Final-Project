from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime, timedelta
from include.usgs_pipeline import create_and_run_pipeline
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig
with DAG(
    'usgs_dag',
    default_args={
        'start_date': datetime(2026,4,1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule='@hourly',
    catchup=False
) as dag:
    run_pipeline = PythonOperator(
        task_id='run_pipeline',
        python_callable=create_and_run_pipeline
    )
    dbt_build = BashOperator(
        task_id='dbt_build',
        bash_command='cd /usr/local/airflow/usgs_earthquake_dbt && dbt build --profiles-dir .'
    )
    run_pipeline >> dbt_build