import os

PROD_DB_NAME = os.getenv('PROD_DB_NAME')
PROD_DB_USER = os.getenv('PROD_DB_USER')
PROD_DB_PASSWORD = os.getenv('PROD_DB_PASSWORD')
PROD_DB_HOST = os.getenv('PROD_DB_HOST')
PROD_DB_PORT = os.getenv('PROD_DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': PROD_DB_NAME,
        'USER': PROD_DB_USER,
        'PASSWORD': PROD_DB_PASSWORD,
        'HOST': PROD_DB_HOST,
        'PORT': PROD_DB_PORT,
    }
}
