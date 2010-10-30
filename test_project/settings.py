import os
BASE = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

SITE_ID = 1

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(BASE, 'adminfiles-test.db')

MEDIA_ROOT = os.path.join(BASE, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'
SECRET_KEY = '6wk#pb((9+oudihdco6m@#1hmr1qp#k+7a=p7c@#z91_^=en-!'

ROOT_URLCONF = 'test_project.urls'

FIXTURE_DIRS = [
    os.path.join(BASE, 'fixtures')
    ]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'adminfiles',
    'sorl.thumbnail',
    'testapp',
    'oembed',
)
