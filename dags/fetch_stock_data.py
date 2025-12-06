import os
import logging
import requests
import psycopg2
from datetime import datetime
from psycopg2.extras import execute_values


def get_db_connection():
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        dbname="crypto_db",
        user="postgres",
        password="postgres"
    )
    return conn


def ensure_table_exists(conn):
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS crypto_prices (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(50) NOT NULL,
        price NUMERIC,
        ts_utc TIMESTAMPTZ NOT NULL,
        CONSTRAINT unique_symbol_ts UNIQUE (symbol, ts_utc)
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_sql)
        conn.commit()


def fetch_and_store_crypto(**kwargs):
    logging.info("Fetching Bitcoin price from Yahoo Finance API")

    url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
    params = {"interval": "1h"}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logging.error("API Request Failed: %s", str(e))
        raise

    try:
        result = data["chart"]["result"][0]
        timestamp = result["timestamp"][-1]
        close_price = result["indicators"]["quote"][0]["close"][-1]
    except Exception:
        logging.error("Error parsing JSON response")
        raise

    if close_price is None:
        logging.warning("Received null price - skipping record")
        return "Skipped"

    ts = datetime.utcfromtimestamp(timestamp).isoformat()

    conn = None
    try:
        conn = get_db_connection()
        ensure_table_exists(conn)

        with conn.cursor() as cur:
            execute_values(
                cur,
                """
                INSERT INTO crypto_prices (symbol, price, ts_utc)
                VALUES %s
                ON CONFLICT (symbol, ts_utc)
                DO UPDATE SET price = EXCLUDED.price;
                """,
                [("BTC-USD", close_price, ts)]
            )
        conn.commit()
        logging.info("Inserted BTC price: %s", close_price)
    except Exception as e:
        logging.error("DB Error: %s", str(e))
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()

    return "Success"
