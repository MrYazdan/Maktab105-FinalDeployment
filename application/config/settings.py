from pathlib import Path
from decouple import config

USE_TZ = True
USE_I18N = True
LANGUAGE_CODE = "en-us"
LOGIN_URL = "/auth/login"
ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "user.User"
WSGI_APPLICATION = "config.wsgi.application"
TIME_ZONE = config("TIME_ZONE", default="UTC")
DEBUG = config("DEBUG", cast=bool, default=True)
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "apps"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = config("SECRET_KEY", default="secret-key-!!!")
AUTHENTICATION_BACKENDS = ["apps.user.backend.ModelBackend"]

ALLOWED_HOSTS = (
    ["*"]
    if DEBUG
    else config(
        "ALLOWED_HOSTS", cast=lambda host: [h.strip() for h in host.split(",") if h]
    )
)

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ]
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Applications
APPLICATIONS = ["core", "user", "post"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "taggit",
    "rest_framework",
    "corsheaders",
    # Application
    *list(map(lambda app: f"apps.{app}", APPLICATIONS)),
]

# Serving
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "storage/static"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "storage/media"

# Mode Handling:
if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True
    # STATICFILES_DIRS = [BASE_DIR / "storage/static"]

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
            "LOCATION": BASE_DIR / "tmp/cache",
        }
    }

    EMAIL_USE_TLS = False
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 25
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    DEFAULT_FROM_EMAIL = "noreply@maktab105.dev"

else:
    REDIS_HOST = config('REDIS_HOST')
    REDIS_PORT = config('REDIS_PORT')
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

    # EMAIL_USE_TLS = config("EMAIL_USE_TLS")
    # EMAIL_USE_SSL = config("EMAIL_USE_SSL")
    # EMAIL_HOST = config("EMAIL_HOST")
    # EMAIL_PORT = config("EMAIL_PORT")
    # EMAIL_HOST_USER = config("EMAIL_USER")
    # EMAIL_HOST_PASSWORD = config("EMAIL_PASSWORD")
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
    CELERY_TIMEZONE = TIME_ZONE
    CELERY_BROKER_URL = REDIS_URL + '/0'
    CELERY_BROKER_BACKEND = REDIS_URL + '/1'
    CELERY_RESULT_BACKEND = REDIS_URL + '/2'
