release: python manage.py migrate
web: gunicorn driver_health.wsgi --log-file -
worker: python manage.py runworker channel_layer
