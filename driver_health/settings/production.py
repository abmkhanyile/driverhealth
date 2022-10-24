from .base_settings import *

DEBUG = False

ALLOWED_HOSTS = ['http://localhost:8000/', 'https://driver-training.herokuapp.com', 'driver-training.herokuapp.com', 'https://www.driverhealth.co.za', 'www.driverhealth.co.za', 'http://www.driverhealth.co.za', 'driverhealth.co.za']


REDIS_TLS_URL = os.environ.get('REDIS_TLS_URL')
REDIS_URL = os.environ.get('REDIS_URL')


import ssl

ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False

heroku_redis_ssl_host = {
    'address': os.environ.get("REDIS_TLS_URL"),  # The 'rediss' schema denotes a SSL connection.
    'ssl': ssl_context
}


# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             "hosts": (heroku_redis_ssl_host,)
#         },
#     },
# }

if os.getcwd() == '/app':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    DEBUG = False