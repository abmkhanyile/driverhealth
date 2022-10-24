from django.conf import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = 'rpc://'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = settings.TIME_ZONE
enable_utc = True