import os

TEST_DB_NAME = os.getenv('TEST_DB_NAME')
TEST_DB_USER = os.getenv('TEST_DB_USER')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
TEST_DB_HOST = os.getenv('TEST_DB_HOST')
TEST_DB_PORT = os.getenv('TEST_DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': TEST_DB_NAME,
        'USER': TEST_DB_USER,
        'PASSWORD': TEST_DB_PASSWORD,
        'HOST': TEST_DB_HOST,
        'PORT': TEST_DB_PORT,
    }
}
