from django.apps import AppConfig

class SubjectsConfig(AppConfig):
    """
    A class to configure subjects for a system.
    
        Class Attributes:
        - default_auto_field: The default auto field for subjects.
        - name: The name of the subject.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
