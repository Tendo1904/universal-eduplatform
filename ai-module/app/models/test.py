from pydantic import BaseModel
from typing import List, Dict

class Question(BaseModel):
    """
    Class representing a question with text and options.
    
        Attributes:
        - question_text: a string representing the text of the question.
        - options: a list containing the available options for the question.
    """

    question_text: str
    options: List[str]

class Test(BaseModel):
    """
    Class to represent a test object.
    
        Class Attributes:
        - id
        - theme
        - questions
    """

    id: int
    theme: str
    questions: List[Question]