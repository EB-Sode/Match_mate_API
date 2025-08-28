from django.apps import AppConfig


class MatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'match'

class FixturesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fixtures'

    def ready(self):
        try:
            import match.signals  # 👈 make sure signals are registered
        except ModuleNotFoundError:
            pass  # or log an error if desired
