from django.apps import AppConfig


class SubjectsConfig(AppConfig):
    """
    This class represents the configuration settings for subjects in a system.
        It provides methods for managing subjects and their attributes.
    
        Class Attributes:
        - default_auto_field: The default field to be used for automatic primary key generation.
        - name: The name of the subject.
    
        Methods:
        - create(subject_data): Creates a new subject using the provided data.
        - update_subject(subject_data): Updates an existing subject with the provided data.
        - delete_subject(subject_id): Deletes the subject with the given ID.
        - get_subject(subject_id): Retrieves the subject with the given ID.
        - list_subjects(): Returns a list of all subjects in the system.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'
