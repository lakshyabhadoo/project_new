# project_new

The project will require a running instance of:

redis (redis-server)
celery -A app.celery_worker.celery_work worker --loglevel=info

running parallelly before running python3 run.py
