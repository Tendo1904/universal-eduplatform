from pydantic import BaseModel, Field


class CreateThemeRequest(BaseModel):
    """
    Represents a request to create a new theme.

        This class is used to encapsulate the details needed for creating a theme, including its name and description.

        Attributes:
            name: The name of the theme.
            descr: A description of the theme.

        Methods:
            (No methods defined for this class.)
    """

    name: str = Field(..., example="Искусственный интеллект")
    descr: str = Field(
        ..., example="Зачем и как ИИ нужен и может использоваться для обучения?"
    )


class ThemeResponse(BaseModel):
    """
    Represents a response for a theme in the application.

        This class is used to encapsulate the details of a theme, including its
        identifier, name, and description.

        Attributes:
            id: The unique identifier of the theme.
            name: The name of the theme.
            descr: A brief description of the theme.
    """

    id: int = Field(..., example=1)
    name: str = Field(..., example="Про ИИ")
    descr: str = Field(..., example="")
