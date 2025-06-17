from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class TestListViewTests(TestCase):
    """
    A class to test the list view for retrieving tests in the API.

    This class provides unit tests to ensure that the API's endpoints
    for listing tests are functioning correctly.

    Methods:
        setUp
        test_get_tests
        test_get_test

    Attributes:
        None

    The methods in this class include:
        - setUp: Prepares the test environment by creating an API client
          and necessary test instances.
        - test_get_tests: Validates the GET operation for retrieving
          a list of tests, asserting a 200 OK response status.
        - test_get_test: Validates the GET request for a specific test
          by asserting a 200 OK response status.
    """

    def setUp(self):
        """
        Sets up the test environment by instantiating an API client and creating a test instance.

            This method initializes an API client and creates a Test object with predefined attributes
            necessary for running tests within the class.

            Parameters:
                None

            Returns:
                None: This method does not return a value.
        """
        self.client = APIClient()
        self.test = Test.objects.create(
            author_id=1, subject_id=1, theme_id=1, expert_id=1, max_points=100
        )

    def test_get_tests(self):
        """
        Tests the 'get' operation for retrieving a list of tests.

            This method performs an HTTP GET request to retrieve a list of tests
            associated with a specific subject and theme. It asserts that the
            response status code is 200 OK, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("test-list", kwargs={"subject_id": 1, "theme_id": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_test(self):
        """
        Tests the GET request for a specific test.

            This method performs a GET request to retrieve a test identified by its primary key (pk)
            and asserts that the HTTP response status code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(reverse("test-get", kwargs={"pk": self.test.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
