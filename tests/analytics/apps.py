from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """
    A class for handling analytics configuration settings.
    
        Attributes:
        - api_key: A string representing the API key used for analytics.
        - tracking_id: A string representing the tracking ID for analytics.
    
        Methods:
        - __init__: Initializes the AnalyticsConfig class with provided API key and tracking ID.
        - set_api_key: Sets a new API key for analytics configuration.
        - set_tracking_id: Sets a new tracking ID for analytics configuration.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'
