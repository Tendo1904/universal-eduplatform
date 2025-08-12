from django.db import models


class Test(models.Model):
    """
    This class represents a Test object that contains information about a particular test, such as author ID, subject ID, theme ID,
        times solved, expert ID, and maximum points.
    
        Class Attributes:
        - author_id
        - subject_id
        - theme_id
        - times_solved
        - expert_id
        - max_points
    """

    author_id = models.IntegerField(null=False, blank=False)
    subject_id = models.IntegerField(null=False, blank=False)
    theme_id = models.IntegerField(null=False, blank=False)
    times_solved = models.IntegerField(default=0, null=False, blank=False)
    expert_id = models.IntegerField(default=0, null=False, blank=False)
    max_points = models.IntegerField(default=0, null=False, blank=False)

    class Meta:
        app_label = 'tests'


class Question(models.Model):
    """
    This class represents a question object for a quiz. It includes information about the question text, additional information, and points associated with the question.
    
        Class Attributes:
        - question_text: represents the text of the question.
        - addition_info: includes any additional information related to the question.
        - question_points: defines the points assigned to the question.
    """

    id_test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=100, null=False, blank=False)
    addition_info = models.TextField(null=False, blank=False)
    question_points = models.IntegerField(default=1, null=False, blank=False)

    class Meta:
        app_label = 'tests'


class Answer(models.Model):
    """
    This class represents an answer to a question.
    
        Class Attributes:
        - answer_text: The text of the answer.
        - id_question: The ID of the question this answer belongs to.
        - is_correct: A boolean indicating if the answer is correct.
    """

    answer_text = models.TextField(null=False, blank=False)
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField()

    class Meta:
        app_label = 'tests'


class Result(models.Model):
    """
    Class Result represents a result object for a specific test taken by a user.
    
        Attributes:
        - id_user: The user ID associated with the result.
        - id_test: The test ID associated with the result.
        - subject: The subject of the test.
        - theme: The theme of the test.
        - points_user: The points scored by the user in the test.
    """

    id_user = models.IntegerField(null=False, blank=False)
    id_test = models.ForeignKey(Test, on_delete=models.CASCADE)
    subject = models.TextField(null=False, blank=False)
    theme = models.TextField(null=False, blank=False)
    points_user = models.FloatField(null=True, blank=True)

    class Meta:
        app_label = 'tests'


class Solutions(models.Model):
    """
    Solutions class provides a structure for storing and managing different solutions associated with questions in a question-answer system.
    
        Class Attributes:
        - id_result: Identifies the result associated with the solution.
        - id_question: Identifies the question for which the solution is provided.
        - user_answer: Represents the answer provided by the user for the question.
    """

    id_result = models.ForeignKey(Result, on_delete=models.CASCADE, related_name='solutions')
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.TextField(null=False, blank=False)

    class Meta:
        app_label = 'tests'