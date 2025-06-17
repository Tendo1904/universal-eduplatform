from fastapi import APIRouter, HTTPException
from app.schemas.theme import CreateThemeRequest, ThemeResponse
from app.services.theme import (
    create_theme,
    delete_theme,
    get_all_themes,
    get_theme_by_id,
)

from typing import List

router = APIRouter()


@router.post("/create", response_model=ThemeResponse, summary="Create theme")
async def create_new_theme(request: CreateThemeRequest):
    """
    Create a new theme.

        This method handles the creation of a new theme based on the provided request data.
        It processes the request asynchronously and returns the created theme response or raises
        an HTTP exception in case of an error.

        Args:
            request: The request object containing information needed to create a new theme.

        Returns:
            A ThemeResponse object representing the created theme.

        Raises:
            HTTPException: If an error occurs during the theme creation process.
    """
    try:
        return await create_theme(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{theme_id}", summary="Delete theme by id")
async def delete_existing_theme(theme_id: int):
    """
    Delete a theme by its ID.

        This method handles the deletion of a theme specified by its unique identifier.
        It attempts to delete the theme and returns a success message upon successful deletion.
        If an error occurs during the deletion process, an HTTPException is raised with an appropriate error message.

        Args:
            theme_id: The unique identifier of the theme to be deleted.

        Returns:
            A dictionary containing a detail message indicating the result of the deletion operation.
    """
    try:
        await delete_theme(theme_id)
        return {"detail": "Theme deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get-all", response_model=List[ThemeResponse], summary="Get all themes")
async def create_new_theme():
    """
    Creates a new theme and retrieves all themes.

        This method handles the request to create a new theme and returns
        a list of all available themes. If an error occurs during the
        retrieval process, it raises an HTTP exception.

        Returns:
            A list of ThemeResponse objects representing all the themes.

        Raises:
            HTTPException: If there is an error in retrieving the themes.
    """
    try:
        return await get_all_themes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/get/{theme_id}", response_model=ThemeResponse, summary="Get theme by id")
async def create_new_theme(theme_id):
    """
    Fetch a theme by its identifier.

        This method retrieves a theme based on the provided theme identifier.
        If the theme is found, it returns the corresponding theme data.
        In case of an error during the retrieval, it raises an HTTPException with a server error status.

        Args:
            theme_id: The unique identifier of the theme to be fetched.

        Returns:
            The theme data corresponding to the given theme identifier.

        Raises:
            HTTPException: An exception that indicates a server error occurred
            during the theme retrieval process.
    """
    try:
        return await get_theme_by_id(theme_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
