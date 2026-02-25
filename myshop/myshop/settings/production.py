from .base import *
import os

# ----------------------------------------------------------------------------
# CORE
# ----------------------------------------------------------------------------

DEBUG = os.environ.get("DEBUG", "0") == "1"

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", SECRET_KEY)

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1"
).split(",")

# ----------------------------------------------------------------------------
# DATABASE (PostgreSQL container)
# ----------------------------------------------------------------------------

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "myshop"),
        "USER": os.environ.get("POSTGRES_USER", "myshop"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "myshoppassword"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": 5432,
    }
}

# ----------------------------------------------------------------------------
# STATIC & MEDIA
# ----------------------------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ----------------------------------------------------------------------------
# SECURITY
# ----------------------------------------------------------------------------

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ----------------------------------------------------------------------------
# REDIS
# ----------------------------------------------------------------------------

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = 6379
REDIS_DB = 1

# ----------------------------------------------------------------------------
# CELERY (RabbitMQ container)
# ----------------------------------------------------------------------------

CELERY_BROKER_URL = os.environ.get(
    "CELERY_BROKER_URL",
    "amqp://guest:guest@rabbitmq:5672//"
)

CELERY_RESULT_BACKEND = os.environ.get(
    "CELERY_RESULT_BACKEND",
    "rpc://"
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"

# ----------------------------------------------------------------------------
# EMAIL
# ----------------------------------------------------------------------------

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"

# ----------------------------------------------------------------------------
# STRIPE
# ----------------------------------------------------------------------------

STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = os.environ.get("STRIPE_API_VERSION")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]