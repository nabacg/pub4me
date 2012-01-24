# Django settings for PubsProject project.
import os

ROOT = lambda base : os.path.join(os.path.dirname(__file__), base).replace('\\','/')

''' 
Zeby uruchomic aplikacje lokalnie nalezy:
1. Ustawic DEBUG = True
2. Zakomentowac namiar na odpowiednia baze

Zeby uruchomic aplikacje na serwerze nalezy:
1. Ustawic DEBUG = False
2. Zakomentowac namiar na odpowiednia baze
'''

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

#TEST !!!!!!!!!!!!!!!!!!!!!!!!!!!!

MANAGERS = ADMINS
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pg4030_pub4me',  # Or path to database file if using sqlite3.
        'USER': 'pg4030_pub4me_user',                      # Not used with sqlite3.
        'PASSWORD': 'czesio',                  # Not used with sqlite3.
        'HOST': 'pgsql.rootnode.net',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pub4me_database',  # Or path to database file if using sqlite3.
        'USER': 'pub4me_user',                      # Not used with sqlite3.
        'PASSWORD': 'czesio',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#MEGITEAM pierwsza baza na megiteam, aktualnie nieuzywana
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pg_4231',  # Or path to database file if using sqlite3.
        'USER': 'pg_4231u',                      # Not used with sqlite3.
        'PASSWORD': 'czesio',                  # Not used with sqlite3.
        'HOST': 'sql.gmc.megiteam.pl',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5435',                      # Set to empty string for default. Not used with sqlite3.
    }
}
# baza testowa megiteam
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pg_4620',  # Or path to database file if using sqlite3.
        'USER': 'pg_4620u',                      # Not used with sqlite3.
        'PASSWORD': 'czesio',                  # Not used with sqlite3.
        'HOST': 'sql.gmc.megiteam.pl',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5435',                      # Set to empty string for default. Not used with sqlite3.
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'pub4me.sqlite',  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Integracja z Facebookiem
FACEBOOK_APP_ID = '153211921382271'
FACEBOOK_APP_SECRET = '9cff3c88942fa6a35fdc706f090ead5a'

GUEST_USER_AUTO_PASSWORD = 'automatyczne_haslo_goscia_666_*&^$%^%$@#%'

AUTH_PROFILE_MODULE = 'pub4me.PubUser'

#potrzebne do tworzenia knajp
DEFAULT_CITY_ID = 'CRACOW'
DEFAULT_EXT_SERVICE_ID = -11

CACHE_BACKEND = 'locmem://?timeout=6"'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4=p%o5*3)7wf92*k6o0!x3o#m4&z=v-d%+&t*69xyv6ek%l)q8'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    ROOT('templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'pub4me',
    'django_extensions',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

#Moze z czasem, z powodow wydajnosciowych, trzeba bedzie cache'owac sesje:
#SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'