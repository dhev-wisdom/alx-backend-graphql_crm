import datetime
import requests

def log_crm_heartbeat():
    """Logs a heartbeat message and optionally checks GraphQL hello field."""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{now} CRM is alive\n"
    log_file = "/tmp/crm_heartbeat_log.txt"
    with open(log_file, 'a') as f:
        f.write(log_message)

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": {"hello"}},
            timeout=5
        )
        if response.status_code == 200:
            with open(log_file, 'a') as f:
                f.write(f"{now} GraphQL responded: {response.json()}\n")
    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"{now} GraphQL check failed: {e}\n")

def update_low_stock():
    """Runs the GraphQL mutation to restock low-stock products and logs results."""
    now = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/low_stock_updates_log.txt"

    mutation = """
    mutation {
        updateLowStockProducts {
            success
            message
            updatedProducts {
                id
                name
                stock
            }
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": {mutation}},
            timeout=10
        )
        result = response.json()

        with open(log_file, 'a') as f:
            f.write(f"{now} - Stock update result: {result}\n")
    except Exception as e:
        with open(log_file, 'a') as f:
            f.write(f"{now} - ERROR: {str(e)}\n")