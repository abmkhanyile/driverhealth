release: python manage.py migrate
#web: gunicorn driver_health.wsgi --log-file -
worker: celery -A driver_health worker -l INFO
