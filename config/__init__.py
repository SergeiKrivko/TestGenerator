try:
    from config.secret import *
    secret_data = False
except ImportError:
    secret_data = False

ORGANISATION_NAME = "SergeiKrivko"
ORGANISATION_URL = "https://github.com/SergeiKrivko/TestGenerator"
APP_NAME = "TestGenerator"
APP_VERSION = "1.5.7"