from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class TestCreateRequest(BaseModel):
    """
    A class to handle the creation of test requests.

    Attributes:
        theme: The theme associated with the test request.
        options: Options available for the test request.

    Methods:
        __init__: Initializes a TestCreateRequest instance.
        create_request: Creates a new test request based on the provided theme and options.
        validate_request: Validates the parameters for the test request.
    """

    theme: int = Field(..., example=1)
    options: Optional[str] = Field(
        None, example="Create 4 questions with 1 right answer"
    )


class TestCreateResponse(BaseModel):
    """
    A class for creating and managing test responses.

        This class is designed to facilitate the creation and management of responses
        for test questions, allowing users to handle themes, questions, and corresponding answers.

        Attributes:
            theme: The theme or subject of the test.
            question: The specific question being addressed in the test.
            answers: The list of possible answers to the question.

    """

    theme: int = Field(..., example=1)
    question: str = Field(
        ..., example="Где ИИ повышает эффективность обучения? (несколько)?"
    )
    answers: List[Dict] = Field(
        ...,
        example=[
            {"Анализ успеваемости": "t"},
            {"Персональные тесты": "t"},
            {"Соцсети без учёбы": "f"},
            {"Виртуальные лаборатории": "f"},
        ],
    )


class TestPassRequest(BaseModel):
    """
    Represents a request to pass a test with a set of themes, questions, and answers.

    Attributes:
        theme: The theme of the test.
        question: The question being asked in the test.
        answers: The possible answers to the question provided in the test.

    Methods:
        (If applicable, list method names here)

    This class is structured to hold the necessary information for a test request,
    including the theme of the test, the question to be answered, and the available
    options for answers. The methods (if implemented) will operate on these attributes
    to facilitate test processing and validation.
    """

    theme: int = Field(..., example=1)
    question: str = Field(..., example="Где ИИ улучшает доступность обучения?")
    answers: List[str] = Field(
        ...,
        example=[
            "Субтитры",
            "Озвучка",
            "Физический контроль",
            "Персональные ассистенты",
        ],
    )


class TestPassResponse(BaseModel):
    """
    Represents a response to a test pass, encapsulating the outcome of a test evaluation.

    Attributes:
        right_answers: A collection of correct answers for the test.

    Methods:
        (No methods defined)

    The TestPassResponse class is used to manage the results of a test, particularly focusing on
    the correct responses that are identified. It is designed to facilitate further operations
    related to test evaluations and assessments.
    """

    right_answers: List[str] = Field(..., example=["A", "C"])
