from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    This class represents the configuration for users in the system.
    
        Class Attributes:
        - default_auto_field
        - name
    
        Methods:
        - None
    
        Attributes:
        The attributes `default_auto_field` and `name` are explicitly set in the object's constructor method.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
