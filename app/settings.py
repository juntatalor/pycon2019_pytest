import os
from distutils.util import strtobool


class Config:
    DATABASE_URL = os.environ.get('DATABASE_URL', '')
    PORT = int(os.environ.get('PORT', 8000))
    DEBUG = strtobool(os.environ.get('DEBUG', 'false'))
