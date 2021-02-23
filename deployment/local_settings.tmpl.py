CELERY_TASK_TIME_LIMIT = 10 * 60
CELERY_BROKER_URL = "redis://redis:6379"
CELERY_ALWAYS_EAGER = False
ENTREZ_EMAIL = "{{ entrez_email }}"

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ database_name }}',
        'USER': '{{ database_user }}',
        'PASSWORD': '{{ database_password }}',
        'HOST': '{{ database_host }}',
        'PORT': 3306
    }
}
