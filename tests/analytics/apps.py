from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """
    Configuration class for analytics-related settings.

        This class defines the configuration for the analytics application,
        including default settings used throughout the analytics module.

        Attributes:
            default_auto_field: The default auto field for the model.
            name: The name of the application as it is recognized in the Django project.

        Methods:
            (No methods defined in this class.)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "analytics"
