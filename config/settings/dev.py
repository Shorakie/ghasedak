from .base import *

DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = ['*']

LOGGING = {}
