from peewee import Model, AutoField, CharField, TextField
from app.config import db


class Theme(Model):
    """
    A class to represent a theme in the application.

    This class encapsulates the properties and behaviors of a theme,
    allowing for the management and customization of various theme
    features.

    Attributes:
        id: A unique identifier for the theme.
        name: The name of the theme.
        descr: A brief description of the theme.

    Methods:
        (If there are any methods, list them here without details.)
    """

    id = AutoField()
    name = CharField(max_length=255)
    descr = TextField()

    class Meta:
        database = db
        table_name = "themes"
