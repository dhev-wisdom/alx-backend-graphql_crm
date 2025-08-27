# CRM Celery Setup

## Requirements
- Redis
- Celery
- django-celery-beat

## Installation
```bash
pip install -r requirements.txt
```

# Redis Setup

## Start Redis locally:
```bash
redis-server
```

## Database Setup
```bash
python manage.py migrate
```

## Run Celery

Start a worker:
```bash
celery -A crm worker -l info
```

Start Celery Beat:
```bash
celery -A crm beat -l info
```

## Verify

Check logs:
```bash
cat /tmp/crm_report_log.txt
```

Reports will appear weekly (Monday 6AM):
```bash
2025-08-25 06:00:00 - Report: 20 customers, 50 orders, 1,250.00 revenue
```

---

✅ This gives you:  
- A **weekly Celery Beat job** every Monday at 6AM.  
- Uses **GraphQL query** for customers, orders, revenue.  
- Logs results in `/tmp/crm_report_log.txt`.  

---