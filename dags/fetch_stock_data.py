# dags/fetch_stock_data.py

def fetch_and_store_stock(**kwargs):
    """
    Minimal placeholder task.

    In a full version, this function would:
    - Call an external stock market API
    - Parse the JSON response
    - Store or update rows in a database

    For this simplified assignment version, it just prints a message.
    """
    print("Running minimal fetch_and_store_stock task...")
    print("Here we would fetch data from an API and store it into a database.")
    return "ok"
