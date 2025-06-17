from pydantic_settings import BaseSettings
from playhouse.db_url import connect


class Settings(BaseSettings):
    """
    A class to manage configuration settings for the application.

    This class encapsulates essential settings such as the AI model endpoint
    and the database URL, providing a centralized way to access and modify
    these configurations.

    Attributes:
        ai_model_endpoint: The endpoint for the AI model.
        database_url: The URL for the database connection.
    """

    ai_model_endpoint: str = "http://localhost:8001"
    database_url: str = "postgres://user:P@ssw0rd@127.0.0.1:5432/lisa"


settings = Settings()

# инициализируем подключение Peewee по URL
db = connect(settings.database_url)
