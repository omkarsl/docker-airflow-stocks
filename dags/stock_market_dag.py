from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from fetch_crypto_data import fetch_and_store_crypto

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="crypto_price_hourly_pipeline",
    default_args=default_args,
    description="Fetch and store BTC price into PostgreSQL",
    schedule_interval="0 * * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["crypto", "postgres", "api"],
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_and_store_crypto_task",
        python_callable=fetch_and_store_crypto,
    )

    fetch_task
