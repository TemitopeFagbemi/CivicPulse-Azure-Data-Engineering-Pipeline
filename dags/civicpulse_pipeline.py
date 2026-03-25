from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import subprocess

# Default arguments
default_args = {
    "owner": "temi",
    "depends_on_past": False,
    "retries": 1,
}

# DAG definition
with DAG(
    dag_id="civicpulse_end_to_end_pipeline",
    default_args=default_args,
    description="Bronze → Silver → Gold pipeline",
    schedule="@daily",  # change later if needed
    start_date=datetime(2026, 3, 1),
    catchup=False,
) as dag:

    # -------- TASK FUNCTIONS -------- #

    def run_bronze():
        subprocess.run(
            ["python", "/usr/local/airflow/include/load_raw_data_to_bronze_layer.py"],
            check=True
        )

    def run_silver():
        subprocess.run(
            ["python", "/usr/local/airflow/include/load_transformed_data_to_silver_layer.py"],
            check=True
        )

    def load_silver_postgres():
        subprocess.run(
            ["python", "/usr/local/airflow/include/load_silver_to_postgres.py"],
            check=True
        )

    def run_gold():
        subprocess.run(
            ["python", "/usr/local/airflow/include/gold_transformation_to_postgres.py"],
            check=True
        )

    # -------- TASKS -------- #

    bronze_task = PythonOperator(
        task_id="bronze_ingestion",
        python_callable=run_bronze,
    )

    silver_task = PythonOperator(
        task_id="silver_transformation",
        python_callable=run_silver,
    )

    silver_to_pg_task = PythonOperator(
        task_id="load_silver_to_postgres",
        python_callable=load_silver_postgres,
    )

    gold_task = PythonOperator(
        task_id="gold_transformation",
        python_callable=run_gold,
    )

    # -------- DEPENDENCIES -------- #

    task_chain = bronze_task >> silver_task >> silver_to_pg_task >> gold_task