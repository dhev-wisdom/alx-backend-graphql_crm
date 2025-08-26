#!/bin/bash

PROJECT_DIR="C:\\Users\\nonso\\Desktop\\ALX_PRODEV_BACKEND\\Alx-GraphQL\\alx_backend_graphql_crm"
MANAGE_PY="$PROJECT_DIR/manage.py"

LOG_FILE="/tmp/customer_cleanup_log.txt"

DELETED_COUNT=$(python $MANAGE_PY shell -c "
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(orders__isnull=True) | Customer.objects.exclude(orders__order_date__gte=one_year_ago)

inactive_customers = inactive_customers.distinct()

count = inactive_customers.count()

inactive_customers.delete()
print(count)
")

echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
