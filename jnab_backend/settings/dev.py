"""
dev.py — Development environment settings.
Usage: export DJANGO_SETTINGS_MODULE=jnab_backend.settings.dev
"""

from .base import *  # noqa: F401, F403

# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = "django-insecure-dev-only-^arh9#qvqp2n7s1i5jym-y$-2cdv8q_4t%=!gx9-4@z^n%3q5r"

ALLOWED_HOSTS = ["*"]


# ---------------------------------------------------------------------------
# Database — SQLite for local dev (zero config)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# ---------------------------------------------------------------------------
# CORS — open during development
# ---------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# ---------------------------------------------------------------------------
# DRF overrides — add browsable API for easier debugging
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # inherit base config
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Human-readable API in browser
    ],
}


# ---------------------------------------------------------------------------
# Django Debug Toolbar (install separately: pip install django-debug-toolbar)
# ---------------------------------------------------------------------------
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
# INTERNAL_IPS = ["127.0.0.1"]


# ---------------------------------------------------------------------------
# Email — print to console in dev
# ---------------------------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# ---------------------------------------------------------------------------
# Logging — verbose console output for development
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "dev": {
            "format": "[{levelname}] {asctime} {module}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "dev",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",  # Set to DEBUG temporarily to log all SQL queries
            "propagate": False,
        },
    },
}
