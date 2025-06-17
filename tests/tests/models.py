from django.db import models


class Test(models.Model):
    """
    A class representing a test with various attributes related to its identity and performance.

    Attributes:
        author_id: The identifier for the author of the test.
        subject_id: The identifier for the subject the test pertains to.
        theme_id: The identifier for the theme of the test.
        times_solved: The number of times the test has been solved.
        expert_id: The identifier for the expert associated with the test.
        max_points: The maximum points achievable for the test.

    This class encapsulates information about a test, including its authorship, categorization,
    and performance metrics through its attributes. It may also include methods for managing
    test operations, but none are detailed here.
    """

    author_id = models.IntegerField(null=False, blank=False)
    subject_id = models.IntegerField(null=False, blank=False)
    theme_id = models.IntegerField(null=False, blank=False)
    times_solved = models.IntegerField(default=0, null=False, blank=False)
    expert_id = models.IntegerField(default=0, null=False, blank=False)
    max_points = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        app_label = "tests"


class Question(models.Model):
    """
    Represents a question in a test.

        This class is designed to encapsulate the attributes of a question, including the question text,
        any additional information, and the points assigned to the question.

        Attributes:
            id_test: The identifier for the test to which the question belongs.
            question_text: The text content of the question.
            addition_info: Any additional information about the question, such as hints or context.
            question_points: The number of points the question is worth.

        Methods:
            None
    """

    id_test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name="questions"
    )
    question_text = models.CharField(max_length=100, null=False, blank=False)
    addition_info = models.TextField(null=False, blank=False)
    question_points = models.IntegerField(default=1, null=False, blank=False)

    class Meta:
        app_label = "tests"


class Answer(models.Model):
    """
    Represents an answer to a question in a quiz or assessment.

    Attributes:
        answer_text: The text of the answer.
        id_question: The unique identifier for the associated question.
        is_correct: A boolean indicating whether the answer is correct.

    Methods:
        (No methods defined)

    The Answer class is used to encapsulate the details of an answer, including
    the text of the answer, the question it corresponds to, and whether it is
    marked as the correct answer.
    """

    answer_text = models.TextField(null=False, blank=False)
    id_question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    is_correct = models.BooleanField()

    class Meta:
        app_label = "tests"


class Result(models.Model):
    """
    Represents the result of a user's test, encapsulating key details of the test performance.

    Attributes:
        id_user: The identifier for the user who took the test.
        id_test: The identifier for the test that was taken.
        subject: The subject of the test.
        theme: The theme or topic of the test.
        points_user: The total points scored by the user on the test.

    Methods:
        (List of methods would be included here if any were defined)

    The Result class contains attributes that store essential information related to
    a user's test results, including identifiers, subject matter, and the score achieved.
    """

    id_user = models.IntegerField(null=False, blank=False)
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    subject = models.TextField(null=False, blank=False)
    theme = models.TextField(null=False, blank=False)
    points_user = models.FloatField(null=True, blank=True)

    class Meta:
        app_label = "tests"


class Solutions(models.Model):
    """
    A class to represent a collection of solutions to questions.

    This class manages the user's answers to specific questions and tracks
    related identifiers for result and question.

    Attributes:
        id_result: Identifier for the result of the solution.
        id_question: Identifier for the related question.
        user_answer: The user's provided answer to the question.

    Methods:
        (methods will be listed here if any are defined)

    The class provides functionality to store and manage answers
    alongside their corresponding question and result identifiers.
    This can facilitate processes such as evaluation of answers and
    record-keeping for user submissions.
    """

    id_result = models.ForeignKey(
        Result, on_delete=models.CASCADE, related_name="solutions"
    )
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField(null=False, blank=False)

    class Meta:
        app_label = "tests"
