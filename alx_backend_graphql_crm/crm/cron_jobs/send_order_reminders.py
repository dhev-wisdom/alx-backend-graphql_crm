import sys
import os
from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

query = gql("""
query GetRecentOrders($dateFrom: Datetime!) {
    orders(filter: { orderDate_Gte: $dateFrom }) {
        id
        customer { email }    
        orderDate
        }
}
""")

def main():
    date_from = (datetime.now() - timedelta(days=7)).isoformat()

    transport = RequestsHTTPTransport(
        url=GRAPHQL_ENDPOINT,
        verify=True,
        retries=3
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute query
    try:
        result = client.execute(query, variable_values={"dateFrom": date_from})
        orders = result.get("orders", [])

        # Log results
        log_file = "/tmp/order_reminders_log.txt"
        with open(log_file, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n[{timestamp}] Processed {len(orders)} orders\n")
            for order in orders:
                f.write(f"Order ID: {order['id']}, Email: {order['customer']['email']}\n")

        print("Order reminders processed!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()