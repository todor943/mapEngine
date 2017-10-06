from __future__ import unicode_literals

from django.apps import AppConfig

class MapapiConfig(AppConfig):
    name = 'MapApi'

    def ready(self):
        from . import signals