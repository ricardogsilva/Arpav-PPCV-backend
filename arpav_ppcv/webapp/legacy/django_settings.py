# django settings
#
# These are used for:
#
# - setting up the legacy app and also for accessing
# - initializing django and accessing its ORM from the v1 app
#
import os
from pathlib import Path
from typing import Any

import yaml

from ... import config


def get_custom_django_settings(settings: config.ArpavPpcvSettings) -> dict[str, Any]:
    base_dir = str(Path(__file__).parents[3] / "backend")
    time_zone = "UTC"
    if (config_file_path := settings.log_config_file) is not None:
        log_config = yaml.safe_load(Path(config_file_path).read_text())
    else:
        log_config = None
    result = {
        "SECRET_KEY": settings.django_app.secret_key,
        "DEBUG": settings.debug,
        "ALLOWED_HOSTS": ["*"],
        "STATICFILES_FINDERS": (
            "django.contrib.staticfiles.finders.FileSystemFinder",
            "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        ),
        "RESOURCE_ROOT": os.path.join(base_dir, "resources"),
        "INSTALLED_APPS": [
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "django.contrib.staticfiles",
            "django_extensions",
            "django_celery_beat",
            "django_celery_results",
            "oauth2_provider",
            "channels",
            "rest_framework",
            "rest_framework_gis",
            "corsheaders",
            "guardian",
            "django.contrib.gis",
            "djcore.djcore.core",
            "djcore.djcore.users",
            "djcore.djcore.groups",
            "padoa.thredds",
            "padoa.forecastattributes",
            "padoa.places",
        ],
        "MIDDLEWARE": [
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "corsheaders.middleware.CorsMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
            "oauth2_provider.middleware.OAuth2TokenMiddleware",
        ],
        "ROOT_URLCONF": "djangoapp.urls",
        "TEMPLATES": [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [os.path.join(base_dir, "templates")],
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
        ],
        "WSGI_APPLICATION": "djangoapp.wsgi.application",
        "ASGI_APPLICATION": "djangoapp.asgi.app",
        "DATABASES": {
            "default": {
                "ENGINE": settings.django_app.db_engine,
                "NAME": settings.django_app.db_dsn.path[1:],
                "USER": settings.django_app.db_dsn.hosts()[0]["username"],
                "PASSWORD": settings.django_app.db_dsn.hosts()[0]["password"],
                "HOST": settings.django_app.db_dsn.hosts()[0]["host"],
                "PORT": settings.django_app.db_dsn.hosts()[0]["port"],
                "CONN_MAX_AGE": 3600,
            }
        },
        "AUTH_PASSWORD_VALIDATORS": [
            {
                "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
            },
            {
                "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
            },
        ],
        "LANGUAGE_CODE": "en-us",
        "TIME_ZONE": time_zone,
        "USE_I18N": True,
        "USE_L10N": True,
        "USE_TZ": True,
        "AUTH_USER_MODEL": "users.User",
        "STATIC_URL": settings.django_app.static_mount_prefix,
        "STATIC_ROOT": str(settings.django_app.static_root),
        "STATICFILES_DIRS": (os.path.join(base_dir, "templates"),),
        "REST_FRAMEWORK": {
            "COERCE_DECIMAL_TO_STRING": False,
            "DEFAULT_PERMISSION_CLASSES": [
                "rest_framework.permissions.AllowAny",
            ],
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
            ],
            "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
            "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
            "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
            "PAGE_SIZE": 100,
        },
        "CORS_ORIGIN_ALLOW_ALL": True,
        "X_FRAME_OPTIONS": "ALLOWALL",
        "ELASTICSEARCH": {
            "host": "localhost",
            "port": 9200,
        },
        "AUTHENTICATION_BACKENDS": (
            "oauth2_provider.backends.OAuth2Backend",
            "django.contrib.auth.backends.ModelBackend",
            "guardian.backends.ObjectPermissionBackend",
        ),
        "OAUTH2_PROVIDER": {
            "SCOPES": {
                "read": "read",
                "write": "write",
            },
            "OAUTH2_BACKEND_CLASS": "oauth2_provider.oauth2_backends.JSONOAuthLibCore",
            "ACCESS_TOKEN_EXPIRE_SECONDS": 120,
        },
        "DEFAULT_SCOPES": ["read", "write"],
        "LOGIN_URL": "/oauth/login",
        "LOGIN_REDIRECT_URL": "/",
        "EMAIL_HOST": settings.django_app.email.host,
        "EMAIL_HOST_USER": settings.django_app.email.host_user,
        "EMAIL_HOST_PASSWORD": settings.django_app.email.host_password,
        "EMAIL_PORT": settings.django_app.email.port,
        "ACCEPTED_UPLOAD_MEDIA_TYPES": [
            "text/plain",
            "application/x-dbf",
            "application/octet-stream",
            "application/xml",
            "application/pdf",
            "application/zip",
            "image/png",
            "image/tiff",
        ],
        "CELERY_BROKER_URL": settings.django_app.redis_dsn.unicode_string(),
        "CELERY_RESULT_BACKEND": settings.django_app.redis_dsn.unicode_string(),
        "CELERY_ACCEPT_CONTENT": ["json"],
        "CELERY_TASK_SERIALIZER": "json",
        "CELERY_RESULT_SERIALIZER": "json",
        "CELERY_TIMEZONE": time_zone,
        "CACHES": {
            "default": {
                "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
                "LOCATION": "/var/tmp/django_cache",
            }
        },
        "SESSION_ENGINE": "redis_sessions.session",
        "SESSION_REDIS": {
            "host": settings.django_app.redis_dsn.host,
            "port": settings.django_app.redis_dsn.port,
            "db": 0,
            "password": "",
            "prefix": "session",
            "socket_timeout": 1,
        },
        "THREDDS": {
            "host": settings.django_app.thredds.host,
            "auth_url": settings.django_app.thredds.auth_url,
            "port": settings.django_app.thredds.port,
            "user": settings.django_app.thredds.user,
            "password": settings.django_app.thredds.password,
            "proxy": settings.django_app.thredds.proxy,
        },
    }
    if log_config is not None:
        result["LOGGING"] = log_config
    return result
