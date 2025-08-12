from pydantic import BaseModel, Field

class CreateThemeRequest(BaseModel):
    """
    Class represents a request object for creating a theme.
    
        Class Attributes:
        - name: The name of the theme.
        - description: The description of the theme.
    
        Methods:
        No explicit methods defined.
    """

    name: str = Field(..., example="Искусственный интеллект")
    descr: str = Field(..., example="Зачем и как ИИ нужен и может использоваться для обучения?")

class ThemeResponse(BaseModel):
    """
    Class representing a response for a theme, including its id, name, and description.
    
        Class Attributes:
        - id: The unique identifier for the theme.
        - name: The name of the theme.
        - descr: The description of the theme.
    """

    id: int = Field(..., example=1)
    name: str = Field(..., example="Про ИИ")
    descr: str = Field(..., example="")