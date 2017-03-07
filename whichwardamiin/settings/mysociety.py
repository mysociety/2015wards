# load the mySociety config from its special file

import yaml
from .paths import *

config = yaml.load(open(os.path.join(PROJECT_ROOT, 'conf', 'general.yml')))

DEBUG = bool(int(config.get('STAGING')))
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': config.get('MAPIT_DB_NAME'),
        'USER': config.get('MAPIT_DB_USER'),
        'PASSWORD': config.get('MAPIT_DB_PASS'),
        'HOST': config.get('MAPIT_DB_HOST'),
        'PORT': config.get('MAPIT_DB_PORT'),
    }
}

TIME_ZONE = config.get('TIME_ZONE')
SECRET_KEY = config.get('DJANGO_SECRET_KEY')
GOOGLE_ANALYTICS_ACCOUNT = config.get('GOOGLE_ANALYTICS_ACCOUNT')
ALLOWED_HOSTS = config.get('ALLOWED_HOSTS', [])

ELECTION_YEAR = config.get('ELECTION_YEAR')
ELECTION_DATE = config.get('ELECTION_DATE')

COUNTY_TYPE = config.get('COUNTY_TYPE')
GENERATION_CURRENT = int(config.get('GENERATION_CURRENT'))
GENERATION_NEW = int(config.get('GENERATION_NEW'))

# An EPSG code for what the areas are stored as, e.g. 27700 is OSGB, 4326 for
# WGS84. Optional, defaults to 4326.
MAPIT_AREA_SRID = int(config.get('AREA_SRID', 4326))

# Country is currently one of GB, NO, KE or ZA. Optional; country specific things
# won't happen if not set.
MAPIT_COUNTRY = config.get('COUNTRY', '')

MAPIT_RATE_LIMIT = []
