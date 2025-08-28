from django.apps import AppConfig


class PredictionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictions'

    def ready(self):
        try:
            import predictions.signals  # 👈 make sure signals are registered
        except ModuleNotFoundError:
            pass  # or log an error if desired
