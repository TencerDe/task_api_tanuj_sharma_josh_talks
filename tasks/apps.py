from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Configuration class for the tasks application.
    Specifies the default auto field and application name.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
