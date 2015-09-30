"""
Configuration file for py.test
"""

import django


def pytest_configure():
    from django.conf import settings
    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "test.sqlite3",
            }
        },
        ROOT_URLCONF="elasticstack.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            "haystack",
            "elasticstack",
        ],
        HAYSTACK_CONNECTIONS={
            'default': {
                'ENGINE': 'elasticstack.backends.ConfigurableElasticSearchEngine',
                'URL': 'http://127.0.0.1:9200/',
                'INDEX_NAME': 'haystack',
            },
        },
        MIDDLEWARE_CLASSES=(),
        SITE_ID=1,
    )
    try:
        django.setup()
    except AttributeError:
        pass
