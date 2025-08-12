from fastapi import APIRouter, HTTPException
from app.schemas.theme import CreateThemeRequest, ThemeResponse
from app.services.theme import create_theme, delete_theme, get_all_themes, \
    get_theme_by_id

from typing import List

router = APIRouter()

@router.post("/create",
             response_model=ThemeResponse,
             summary="Create theme")
async def create_new_theme(request: CreateThemeRequest):
    """
    Creates a new theme based on the provided request data.
    
    Args:
    - request: The request object containing the data for the new theme.
    
    Return:
    - The response model for the newly created theme.
    
    Notes:
    This method is decorated with '@router.post' with route '/create' and response model 'ThemeResponse' for creating a theme.
    """
    try:
        return await create_theme(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{theme_id}",
               summary="Delete theme by id")
async def delete_existing_theme(theme_id: int):
    """
    Deletes an existing theme by its ID.
    
    Args:
    - theme_id: The ID of the theme to be deleted.
    
    Returns:
    Dictionary with a detail key indicating the success message after deleting the theme.
    """
    try:
        await delete_theme(theme_id)
        return {"detail": "Theme deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get-all",
             response_model=List[ThemeResponse],
             summary="Get all themes")
async def create_new_theme():
    """
    Create a new theme by retrieving all existing themes.
    
    Args:
        None
    
    Returns:
        List[ThemeResponse]: A list of all available themes retrieved successfully.
    
    Raises:
        HTTPException: An error occurred while fetching the themes, with a status code of 500 and the error details.
    """
    try:
        return await get_all_themes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/get/{theme_id}",
             response_model=ThemeResponse,
             summary="Get theme by id")
async def create_new_theme(theme_id):
    """
    Create a new theme by fetching the theme using the provided theme_id.
    
    Args:
    - theme_id: The unique identifier of the theme to be created.
    
    Returns:
    - The theme object with the specified theme_id.
    """
    try:
        return await get_theme_by_id(theme_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))