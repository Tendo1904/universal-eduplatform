from typing import List
from peewee import DoesNotExist
from app.config import db
from app.models.theme import Theme as ThemeModel
from app.schemas.theme import CreateThemeRequest, ThemeResponse

async def create_theme(request: CreateThemeRequest) -> ThemeResponse:
    """
    Create a new theme in the database and return its Pydantic model.
    
    Args:
        request (CreateThemeRequest): The request object containing the details of the theme to be created.
    
    Returns:
        ThemeResponse: The Pydantic model representing the created theme.
    """
    db.connect(reuse_if_open=True)
    theme = ThemeModel.create(name=request.name, descr=request.descr)
    # если нужно сразу сохранить (Peewee обычно сохраняет сразу при .create())
    db.close()
    return ThemeResponse(id=theme.id, name=theme.name, descr=theme.descr)

async def delete_theme(theme_id: int) -> None:
    """
    Удаляем тему по ID. Если темы нет — не даём упасть.
    
    Args:
        theme_id (int): Уникальный идентификатор темы, которую нужно удалить.
    
    Returns:
        None
    """
    db.connect(reuse_if_open=True)
    (ThemeModel
        .delete()
        .where(ThemeModel.id == theme_id)
        .execute()
    )
    db.close()

async def get_all_themes() -> List[ThemeResponse]:
    """
    Returns a list of all themes.
    
    Args:
        No input arguments.
    
    Returns:
        List[ThemeResponse]: A list of ThemeResponse objects containing theme information such as id, name, and description.
    """
    db.connect(reuse_if_open=True)
    themes = [
        ThemeResponse(id=t.id, name=t.name, descr=t.descr)
        for t in ThemeModel.select()
    ]
    db.close()
    return themes

async def get_theme_by_id(theme_id: int) -> ThemeResponse:
    """
    Get a theme by its ID from the database and return its details if found, otherwise raise an exception.
    
    Args:
        theme_id (int): The ID of the theme to retrieve.
    
    Returns:
        ThemeResponse: An object containing the ID, name, and description of the retrieved theme.
    """
    db.connect(reuse_if_open=True)
    try:
        t = ThemeModel.get(ThemeModel.id == theme_id)
    except DoesNotExist:
        db.close()
        raise
    db.close()
    return ThemeResponse(id=t.id, name=t.name, descr=t.descr)