from pydantic import BaseModel
from typing import List, Dict


class Question(BaseModel):
    """
    Represents a multiple-choice question with associated options.

    Attributes:
        question_text: The text of the question.
        options: A list of possible answers for the question.

    Methods:
        (No methods defined in this class.)

    The Question class is designed to encapsulate the information related to a
    multiple-choice question, including the question itself and the available
    answer options. It provides a structured way to manage and present quiz
    questions in an application.
    """

    question_text: str
    options: List[str]


class Test(BaseModel):
    """
    Represents a test with a specific theme and a set of questions.

        This class is used to create and manage a test instance, which
        includes various attributes relevant to the test's identity and content.

        Attributes:
            id: Unique identifier for the test.
            theme: The main subject or topic of the test.
            questions: A collection of questions included in the test.

        Methods:
            (No methods defined in this class)
    """

    id: int
    theme: str
    questions: List[Question]
