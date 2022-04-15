"""Load settings"""

from dotenv import load_dotenv

load_dotenv()

from Samodelkin.settings.base import *

if DEBUG:
    from Samodelkin.settings.dev.rest import REST_FRAMEWORK
else:
    from Samodelkin.settings.prod.rest import REST_FRAMEWORK

if SECURITY_MODE == 'dev':
    from Samodelkin.settings.dev.security import *
elif SECURITY_MODE == 'test':
    from Samodelkin.settings.test.security import *
elif SECURITY_MODE == 'prod':
    from Samodelkin.settings.prod.security import *

if DATABASE_MODE == 'dev':
    from Samodelkin.settings.dev.db import DATABASES
elif DATABASE_MODE == 'test':
    from Samodelkin.settings.test.db import DATABASES
elif DATABASE_MODE == 'prod':
    from Samodelkin.settings.prod.db import DATABASES

if not USE_S3:
    from Samodelkin.settings.dev.upload import *
else:
    from Samodelkin.settings.prod.upload import *
