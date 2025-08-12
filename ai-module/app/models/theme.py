from peewee import Model, AutoField, CharField, TextField
from app.config import db

class Theme(Model):
    """
    The Theme class represents a theme in a software application.
    
        Class Attributes:
        - id: The unique identifier of the theme.
        - name: The name of the theme.
        - descr: A description of the theme.
    """

    id    = AutoField()
    name  = CharField(max_length=255)
    descr = TextField()

    class Meta:
        database = db
        table_name = "themes"