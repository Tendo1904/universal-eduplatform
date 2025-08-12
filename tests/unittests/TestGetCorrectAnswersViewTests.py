from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class GetAllCorrectAnswersViewTests(TestCase):
    """
    Class GetAllCorrectAnswersViewTests:
        This class contains unit tests for the GetAllCorrectAnswersView.
    
        Attributes:
        - question_factory: A factory for creating question objects.
        - question: A question instance.
    
        Class Methods:
        - test_get_correct_answers: Test method for retrieving all correct answers.
        - test_get_correct_answers_by_question: Test method for retrieving correct answers by question.
    """

    def setUp(self):
        """
        Set up the initial test environment with necessary data including creating a test, a question, and an answer.
        
        Args:
        - self: The instance of the class.
        
        Initialized class fields:
        - client: An instance of APIClient.
        - test: A test object with author, subject, theme, expert, max points fields.
        - question: A question object related to the test.
        - answer: An answer object related to the question.
        
        Returns:
        None
        """
        self.client = APIClient()
        self.test = Test.objects.create(
            author_id=1,
            subject_id=1,
            theme_id=1,
            expert_id=1,
            max_points=100
        )
        self.question = Question.objects.create(id_test=self.test, question_text="Sample Question")
        self.answer = Answer.objects.create(id_question=self.question, answer_text="Sample Answer", is_correct=True)

    def test_get_correct_answers(self):
        """
        Test method for retrieving correct answers by sending a GET request to the 'correct-answers' endpoint with the test ID as a parameter.
            
        Parameters:
            - self: the instance of the test case class
                
        Args:
            self: the instance of the test case class
        
        Returns:
            None
        """
        response = self.client.get(reverse('correct-answers', kwargs={'pk': self.test.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correct_answers_by_question(self):
        """
        Summary: Retrieve correct answers by question ID and assert the response status code.
        
        Parameters:
        - self: The instance of the class.
        
        Args:
        - None
        
        Returns:
        - None
        """
        response = self.client.get(reverse('correct-answers-by-question', kwargs={'question_pk': self.question.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)