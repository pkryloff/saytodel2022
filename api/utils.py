import logging
import os
import random
from string import ascii_letters, digits

from Samodelkin.settings import BASE_DIR

logs_path = os.path.join(BASE_DIR, 'logs')


def configure_logger(name, level=logging.DEBUG):
    LOGGER = logging.getLogger(name)
    LOGGER.setLevel(level)

    if not os.path.exists(logs_path):
        os.mkdir(logs_path)

    fh = logging.FileHandler(f'logs/{name}.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    LOGGER.addHandler(fh)
    return LOGGER


def generate_filename(file_ext: str) -> str:
    filename = f'{"".join(random.choice(ascii_letters + digits) for _ in range(15))}.{file_ext}'
    return filename
