from Samodelkin.settings import BACKEND_HOST, FRONTEND_HOST

ALLOWED_HOSTS = [
    f'.{BACKEND_HOST}',
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    f'https://{FRONTEND_HOST}',
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
