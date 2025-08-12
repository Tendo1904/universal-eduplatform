from django.apps import AppConfig


class TestsConfig(AppConfig):
    """
    This class represents the configuration settings for the tests module.
    
        Class Attributes:
        - default_auto_field
        - name
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tests'
