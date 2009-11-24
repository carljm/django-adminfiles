from os.path import dirname, join
TEST_ROOT = dirname(__file__)

INSTALLED_APPS = ('adminfiles', 'tests',
                  'django.contrib.contenttypes',
                  'django.contrib.admin',
                  'django.contrib.sites',
                  'django.contrib.auth',
                  'django.contrib.sessions',
                  'sorl.thumbnail')
DATABASE_ENGINE = 'sqlite3'

SITE_ID = 1

MEDIA_URL = '/media/'
MEDIA_ROOT = join(TEST_ROOT, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = MEDIA_ROOT

ROOT_URLCONF = 'tests.urls'

TEMPLATE_DIRS = (join(TEST_ROOT, 'templates'),)
