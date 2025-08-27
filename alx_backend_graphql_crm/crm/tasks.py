import datetime
import requests
from celery import shared_task

@shared_task
def generate_crm_report():
    """Fetch summary stats from GraphQL and log them."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = "/tmp/crm_report_log.txt"

    query = """
    query {
        customers {
            id
        }
        orders {
            id
            totalAmount
        }
    }
    """

    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": query},
            timeout=10
        )
        data = response.json()["data"]

        total_customers = len(data["customers"])
        total_orders = len(data["orders"])
        total_revenue = sum(float(o["totalAmount"]) for o in data["orders"])

        log_line = f"{now} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open(log_file, "a") as f:
            f.write(log_line)

        return log_line

    except Exception as e:
        error_msg = f"{now} - ERROR: {str(e)}\n"
        with open(log_file, "a") as f:
            f.write(error_msg)
        return error_msg
