import os

from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#v_zpc#rkmxtb0==&m0!*n41^gys**acz^v5^s$yh3e0s@cufg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


INTERNAL_IPS = ['192.168.56.1']

INSTALLED_APPS += (
    'autofixture',
)
