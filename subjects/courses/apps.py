from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    """
    Configuration class for the Subjects application.

        This class is responsible for setting up the configuration related to
        the Subjects application, including database settings and application
        settings.

        Attributes:
            default_auto_field: The default auto field for model IDs.
            name: The name of the application.

        Methods:
            (No methods defined in this class)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "courses"
