from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class TestAPIViewTests(TestCase):
    """
    A test case for testing the API endpoints related to test creation.

    This class contains test methods that validate the functionality of the
    API for adding new tests.

    Methods:
        setUp
        test_add_test

    Attributes:
        None

    The `setUp` method initializes the API client for use in the tests.
    The `test_add_test` method sends a POST request to the 'test-add'
    endpoint to verify that tests can be successfully created.
    """

    def setUp(self):
        """
        Set up the test environment for the test case.

            This method initializes the API client to be used during the tests.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()

    def test_add_test(self):
        """
        Tests the creation of a new test.

            This method sends a POST request to the 'test-add' endpoint with
            a predefined set of data representing a test, and asserts that the
            response status code indicates successful creation.

            Parameters:
                None

            Returns:
                None: The method does not return a value. It asserts that a
                test is successfully created by checking the response status code.
        """
        data = {
            "author_id": 1,
            "subject_id": 1,
            "theme_id": 1,
            "expert_id": 1,
            "max_points": 100,
            "questions": [
                {
                    "question_text": "Sample Question",
                    "answers": [{"answer_text": "Sample Answer", "is_correct": True}],
                }
            ],
        }
        response = self.client.post(reverse("test-add"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
