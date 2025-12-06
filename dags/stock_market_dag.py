from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from fetch_stock_data import fetch_and_store_stock

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="stock_market_hourly_pipeline",
    default_args=default_args,
    description="Minimal stock market pipeline (placeholder logic)",
    schedule_interval="0 * * * *",  # runs every hour
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["stocks", "minimal"],
) as dag:

    fetch_and_store_task = PythonOperator(
        task_id="fetch_and_store_stock_task",
        python_callable=fetch_and_store_stock,
    )

    fetch_and_store_task
