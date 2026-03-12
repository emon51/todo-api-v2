from pathlib import Path
import environ
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, True))
environ.Env.read_env(BASE_DIR / ".env")


def read_secret(name: str, default: str = "") -> str:
    """Read a Docker secret from /run/secrets/ or fall back to env variable."""
    secret_path = Path(f"/run/secrets/{name}")
    if secret_path.exists():
        return secret_path.read_text().strip()
    return env(name.upper(), default=default)


DEBUG = env("DEBUG", default=True)
SECRET_KEY = read_secret("secret_key", default="dev-secret-key")
ALLOWED_HOSTS = ["*"] # Restrict in production

DJANGO_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
]
LOCAL_APPS = [
    "apps.users",
    "apps.todos",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": read_secret("db_name", default="todo_db"),
        "USER": read_secret("db_user", default="todo_user"),
        "PASSWORD": read_secret("db_password", default="todo_password"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
    }
}

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "EXCEPTION_HANDLER": "config.exceptions.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "config.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

TIME_ZONE = "UTC"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"