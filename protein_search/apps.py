from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class ProteinSearchConfig(AppConfig):
    name = 'protein_search'

    def ready(self):
        if not hasattr(settings, "ENTREZ_EMAIL") or not settings.ENTREZ_EMAIL:
            raise ImproperlyConfigured("`ENTREZ_EMAIL` MUST be specified in your settings file.")
