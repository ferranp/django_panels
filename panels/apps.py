from __future__ import unicode_literals

from django.apps import AppConfig

from .register import autodiscover


class PanelsConfig(AppConfig):
    name = "panels"

    def ready(self):
        autodiscover()
