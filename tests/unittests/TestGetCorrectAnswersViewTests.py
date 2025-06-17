from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class GetAllCorrectAnswersViewTests(TestCase):
    """
    Tests for the API view that retrieves all correct answers for tests.

    This class contains unit tests that verify the functionality of
    the API endpoints responsible for fetching correct answers
    associated with specific tests and questions.

    Methods:
        setUp
        test_get_correct_answers
        test_get_correct_answers_by_question

    Attributes:
        None

    The methods are designed to set up the test environment and
    perform assertions on the API responses to ensure that the
    correct answers can be successfully retrieved for both tests
    and individual questions.
    """

    def setUp(self):
        """
        Set up the test environment for the tests.

            This method initializes the API client and creates a test
            instance along with associated question and answer
            objects required for running the tests.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.test = Test.objects.create(
            author_id=1, subject_id=1, theme_id=1, expert_id=1, max_points=100
        )
        self.question = Question.objects.create(
            id_test=self.test, question_text="Sample Question"
        )
        self.answer = Answer.objects.create(
            id_question=self.question, answer_text="Sample Answer", is_correct=True
        )

    def test_get_correct_answers(self):
        """
        Tests the retrieval of correct answers for a specific test.

            This method sends a GET request to the correct answers endpoint using
            the ID of the current test instance and asserts that the response status
            code is 200 OK, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("correct-answers", kwargs={"pk": self.test.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_correct_answers_by_question(self):
        """
        Tests the API endpoint for retrieving correct answers by question ID.

            This method sends a GET request to the 'correct-answers-by-question'
            endpoint, using the ID of a specific question. It then asserts that
            the response status code is 200 OK, indicating that the request was
            successful.

            Returns:
                None: The method does not return any value. It performs an assertion
                to verify the expected behavior of the API endpoint.
        """
        response = self.client.get(
            reverse(
                "correct-answers-by-question", kwargs={"question_pk": self.question.id}
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
