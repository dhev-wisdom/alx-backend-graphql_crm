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
            f.write(f"{now} GrapQL check failed: {e}\n")