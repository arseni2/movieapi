from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _

class ApiappConfig(AppConfig):
    name = 'apiapp'
    verbose_name = _('apiapp')
    def ready(self):
        import apiapp.signals