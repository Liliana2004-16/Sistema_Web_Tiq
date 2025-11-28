# apps/ganaderia/apps.py
from django.apps import AppConfig

class GanaderiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ganaderia'

    def ready(self):
        # importa señales
        import apps.ganaderia.signals  # noqa
