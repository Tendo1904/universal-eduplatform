from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class TestListViewTests(TestCase):
    """
    This class provides test cases for the views of the TestList app including fetching tests and test details.
    
        Class methods:
        - setUp: Set up test data required for the test methods.
        - test_get_tests: Test the functionality of fetching a list of tests.
        - test_get_test: Test the functionality of fetching a single test.
    
        Attributes mentioned explicitly in the constructor docstring:
        - attributes: Attributes related to the test entity.
        - properties: Additional properties related to the test entity.
    """

    def setUp(self):
        """
        Set up the required initial data for the test execution.
        
        Args:
        - self: The instance of the test case.
        
        Initialized Class Fields:
        - client: An instance of APIClient used for API testing.
        - test: An instance of Test created with specific data for testing purposes, including author ID, subject ID, theme ID, expert ID, and maximum points.
        
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

    def test_get_tests(self):
        """
        Performs a test by sending a GET request to retrieve tests for a specific subject and theme.
        
        Args:
        - self: the instance of the class.
        
        Returns:
        None
        """
        response = self.client.get(reverse('test-list', kwargs={'subject_id': 1, 'theme_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_test(self):
        """
        Performs a test for getting a test object using the client.
        
        Args:
            - self: The instance of the class.
        
        Return:
            None
        """
        response = self.client.get(reverse('test-get', kwargs={'pk': self.test.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
