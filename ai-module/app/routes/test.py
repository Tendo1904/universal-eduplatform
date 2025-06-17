from fastapi import APIRouter, HTTPException
from app.schemas.test import (
    TestCreateRequest,
    TestCreateResponse,
    TestPassRequest,
    TestPassResponse,
)
from app.services.test import create_test, pass_test

router = APIRouter()


@router.post(
    "/create", response_model=TestCreateResponse, summary="Create test on theme"
)
async def create_new_test(request: TestCreateRequest):
    """
    Create a new test on the specified theme.

        This method handles the creation of a test by processing the provided
        request data and invoking the appropriate service function to perform
        the creation operation. If an error occurs during the process, it
        raises an HTTP exception with a status code of 500.

        Args:
            request: The request object containing the information required
            to create a new test.

        Returns:
            A response object representing the outcome of the test creation
            process, structured as defined by the TestCreateResponse model.

        Raises:
            HTTPException: If an error occurs during test creation, an
            HTTPException with a status code of 500 is raised.
    """
    try:
        return await create_test(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pass", response_model=TestPassResponse, summary="Pass test on theme")
async def pass_existing_test(request: TestPassRequest):
    """
    Passes an existing test on a specified theme.

        This method is an asynchronous endpoint that processes a request to mark a test as passed.
        It calls an internal function to handle the test passing logic and raises an HTTP exception
        in case of any errors.

        Args:
            request: The request object containing the details of the test to be passed.

        Returns:
            The response containing the result of the test passing operation.

        Raises:
            HTTPException: If there is an error during the processing of the request.
    """
    try:
        return await pass_test(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
