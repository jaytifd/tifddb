from django.apps import AppConfig


class OldDatabaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'old_database'
