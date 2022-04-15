import os

ALLOWED_HOSTS = [
    '127.0.0.1',
    os.environ['WEBSITE_HOSTNAME'],
]

CORS_ALLOW_ALL_ORIGINS = True
