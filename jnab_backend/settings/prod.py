"""
prod.py — Production environment settings.
Usage: export DJANGO_SETTINGS_MODULE=jnab_backend.settings.prod

ALL secrets must be provided via environment variables — never hardcoded.
Required env vars:
    SECRET_KEY          — Django secret key
    ALLOWED_HOSTS       — Comma-separated list of allowed hostnames
    CORS_ALLOWED_ORIGINS — Comma-separated list of allowed frontend origins
    DATABASE_URL        — Full DB connection string (if using PostgreSQL)
    PYTHONANYWHERE_HOST — Your PythonAnywhere domain (e.g. yourname.pythonanywhere.com)
"""

import os
from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Core — never expose secrets in code
# ---------------------------------------------------------------------------
DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]  # Hard fail if not set — intentional

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

# PythonAnywhere host auto-added if set
_pythonanywhere_host = os.environ.get("PYTHONANYWHERE_HOST", "")
if _pythonanywhere_host and _pythonanywhere_host not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_pythonanywhere_host)


# ---------------------------------------------------------------------------
# Database — PostgreSQL recommended for production scalability
# Use DATABASE_URL env var: postgres://user:pass@host:5432/dbname
# Falls back to SQLite if DATABASE_URL is not set (PythonAnywhere free tier)
# ---------------------------------------------------------------------------
_database_url = os.environ.get("DATABASE_URL", "")

if _database_url:
    import dj_database_url  # pip install dj-database-url psycopg2-binary
    DATABASES = {
        "default": dj_database_url.config(
            default=_database_url,
            conn_max_age=600,          # Keep connections alive for 10 min
            conn_health_checks=True,
        )
    }
else:
    # SQLite fallback — fine for PythonAnywhere free tier
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ---------------------------------------------------------------------------
# CORS — only allow your actual frontend domain(s)
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]


# ---------------------------------------------------------------------------
# Security hardening
# ---------------------------------------------------------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Uncomment once you have HTTPS confirmed:
# SECURE_SSL_REDIRECT = True


# ---------------------------------------------------------------------------
# Static files — served by WhiteNoise (no separate static server needed)
# ---------------------------------------------------------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# ---------------------------------------------------------------------------
# Email — configure SMTP for production
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)


# ---------------------------------------------------------------------------
# Cache — use Memcached on PythonAnywhere or Redis elsewhere
# ---------------------------------------------------------------------------
_redis_url = os.environ.get("REDIS_URL", "")
if _redis_url:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": _redis_url,
        }
    }
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        }
    }


# ---------------------------------------------------------------------------
# Logging — structured file + console logging for production
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d}: {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "WARNING",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "api": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
