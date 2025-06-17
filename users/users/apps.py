from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the Users application.

        This class is responsible for configuring the Users application within
        the Django framework.

        Attributes:
            default_auto_field: The default auto field type for model IDs.
            name: The name of the application.

        Methods:
            (no methods defined)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
