from django.apps import AppConfig


class TestsConfig(AppConfig):
    """
    A configuration class for managing test settings in the application.

        This class is responsible for defining the settings related to the
        testing framework used in the application.

        Attributes:
            default_auto_field: The default auto field for model primary keys.
            name: The name of the application or configuration.

    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tests"
