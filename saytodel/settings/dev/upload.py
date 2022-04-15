import os
from pathlib import Path

from Samodelkin.settings.base import BACKEND_HOST

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

MEDIA_FOLDER = 'mediafiles'
MEDIA_URL = f'{BACKEND_HOST}/{MEDIA_FOLDER}/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_FOLDER)
