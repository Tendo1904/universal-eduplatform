from fastapi import APIRouter, HTTPException
from app.schemas.test import TestCreateRequest, TestCreateResponse, TestPassRequest, TestPassResponse
from app.services.test import create_test, pass_test

router = APIRouter()

@router.post("/create",
             response_model=TestCreateResponse,
             summary="Create test on theme")
async def create_new_test(request: TestCreateRequest):
    """
    Creates a new test on the specified theme.
    
    Args:
        - request: The test creation request object containing the necessary information.
    
    Returns:
        - The response after creating the test.
    """
    try:
        return await create_test(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pass",
             response_model=TestPassResponse,
             summary="Pass test on theme")
async def pass_existing_test(request: TestPassRequest):
    """
    Passes an existing test on the theme.
    
    Args:
    - request: The TestPassRequest object containing information about the test to pass.
    
    Returns:
    - TestPassResponse: A response model indicating the result of passing the test.
    
    WHY: The method 'pass_existing_test' handles passing an existing test on the theme within the Universal EduPlatform AI module, ensuring effective management and functionality for testing processes.
    """
    try:
        return await pass_test(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))