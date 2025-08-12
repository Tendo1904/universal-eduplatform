from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class TestCreateRequest(BaseModel):
    """
    Class representing a request object for creating test cases.
    
        Class Attributes:
        - theme: The theme of the test case.
        - options: The options for the test case.
    """

    theme: int = Field(..., example=1)
    options: Optional[str] = Field(None, example="Create 4 questions with 1 right answer")

class TestCreateResponse(BaseModel):
    """
    This class provides functionality to create response objects for test questions.
    
        Class Attributes:
        - theme: The theme of the test question.
        - question: The text of the test question.
        - answers: A list of possible answers for the test question.
    
        Methods:
        No explicit methods defined in this class.
    """

    theme: int = Field(..., example=1)
    question: str = Field(..., example="Где ИИ повышает эффективность обучения? (несколько)?")
    answers: List[Dict] = Field(..., example=[
        {
            "Анализ успеваемости": 't'
        },
        {
            "Персональные тесты": 't'
        },
        {
            "Соцсети без учёбы": 'f'
        },
        {
            "Виртуальные лаборатории": 'f'
        }
    ])

class TestPassRequest(BaseModel):
    """
    Class representing a test pass request where users can submit their answers for evaluation.
    
        Class Attributes:
        - theme: The theme of the test pass request.
        - question: The question prompt for the test pass request.
        - answers: List of answers submitted by users for evaluation.
    """

    theme: int = Field(..., example=1)
    question: str = Field(..., example="Где ИИ улучшает доступность обучения?")
    answers: List[str] = Field(..., example=[
        "Субтитры",
        "Озвучка",
        "Физический контроль",
        "Персональные ассистенты"
    ])

class TestPassResponse(BaseModel):
    """
    This class represents a response to a test pass.
    
            Attributes:
            - right_answers: The number of correct answers in the test pass.
    """

    right_answers: List[str] = Field(..., example=["A", "C"])