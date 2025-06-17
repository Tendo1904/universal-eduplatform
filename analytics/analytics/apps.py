from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    """
    Configuration for the Subjects application.

        This class is responsible for managing the configuration settings
        of the Subjects application, including database field settings
        and application metadata.

        Attributes:
            default_auto_field: The default type of auto-generated field
                for models in this application.
            name: The name of the Subjects application.

        Methods:
            (No methods defined)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "analytics"
