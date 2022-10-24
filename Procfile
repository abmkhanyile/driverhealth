release: python manage.py migrate
web: daphne driver_health.asgi:application --port $PORT --bind 0.0.0.0
