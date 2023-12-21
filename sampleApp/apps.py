from django.apps import AppConfig


class SampleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sampleApp'

    # function allows to handle signals
    def ready(self):
        import sampleApp.signals
