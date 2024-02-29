import os
from sys import argv

try:
    from src.config.secret import *
    secret_data = True
except ImportError:
    secret_data = False

try:
    from src.config.build import *
except ImportError:
    pass


ORGANISATION_NAME = "SergeiKrivko"
ORGANISATION_URL = "https://github.com/SergeiKrivko/TestGenerator"
APP_NAME = "TestGenerator"
APP_VERSION = "1.10.7"

APP_DIR = os.path.split(argv[0])[0]
ASSETS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
