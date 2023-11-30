try:
    from config.secret import *
    secret_data = True
except ImportError:
    secret_data = False

ORGANISATION_NAME = "SergeiKrivko"
ORGANISATION_URL = "https://github.com/SergeiKrivko/TestGenerator"
APP_NAME = "TestGenerator"
APP_VERSION = "1.9.18"
