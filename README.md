# Dockerized Airflow - Minimal Assignment Version

This is a **simplified** version of the Docker + Airflow project,
suitable as a minimal working assignment.

## What it does

- Starts an Apache Airflow instance in Docker.
- Creates a simple DAG: `stock_market_hourly_pipeline`.
- The DAG runs every hour and calls a Python function that just prints messages.

You can later **extend** it to:
- Call a real stock market API
- Store data in PostgreSQL
- Add proper error handling and logging

## How to run

1. Install **Docker Desktop** and make sure it is running.
2. Extract this ZIP to a folder, for example:

   `C:\Users\OMKAR\docker-airflow-stocks`

3. Open **Command Prompt** and run:

   ```bash
   cd C:\Users\OMKAR\docker-airflow-stocks
   docker-compose up --build
   ```

4. Wait until you see logs showing the webserver is running.

5. Open your browser and go to:

   http://localhost:8080

6. Login with:

   - Username: `admin`
   - Password: `admin`

7. In the Airflow UI, enable the DAG named:
   `stock_market_hourly_pipeline`

8. Trigger it manually once and check the logs of the task
   `fetch_and_store_stock_task` — you should see the print messages.

To stop everything, press `Ctrl + C` in the terminal where Docker is running,
or run:

```bash
docker-compose down
```

You can then gradually replace the placeholder logic in `dags/fetch_stock_data.py`
with your full API + database code when you are ready.
