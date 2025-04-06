from django.apps import AppConfig


class BookActionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'book_actions'

    def ready(self):
        import book_actions.signals
