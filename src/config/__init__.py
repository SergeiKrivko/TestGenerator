import os
from sys import argv

try:
    from src.config.secret import *
    secret_data = True
    from src.config.build import *
except ImportError:
    secret_data = False


ORGANISATION_NAME = "SergeiKrivko"
ORGANISATION_URL = "https://github.com/SergeiKrivko/TestGenerator"
APP_NAME = "TestGenerator"
APP_VERSION = "1.10.5"

APP_DIR = os.path.split(argv[0])[0]