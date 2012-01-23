import os
BASE = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

SITE_ID = 1

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME":os.path.join(BASE, 'adminfiles-test.db'),
    }
}

STATIC_URL = ADMINFILES_MEDIA_URL = '/static/'
STATIC_ROOT = os.path.join(BASE, 'static')
MEDIA_ROOT = os.path.join(BASE, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
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
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'adminfiles',
    'sorl.thumbnail',
    'testapp',
    'oembed',
)
