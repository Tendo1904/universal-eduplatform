from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse

class TestAPIViewTests(TestCase):
    """
    Class representing tests for the TestAPIView endpoint.
    
        Class Methods:
        - setUp: None
        - test_add_test: None
    """

    def setUp(self):
        """
        Summary:
            Sets up the test environment by initializing the 'client' attribute with an instance of APIClient.
        
        Args:
            self: Represents the instance of the class.
        
        Returns:
            None
        """
        self.client = APIClient()

    def test_add_test(self):
        """
        Add a test with predefined data using the API and check the response status code.
        
        Parameters:
        self: Reference to the current instance of the class.
        
        Returns:
        None
        
        Args:
        - self: Reference to the current instance of the class.
        
        Return:
        - None
        """
        data = {
            'author_id': 1,
            'subject_id': 1,
            'theme_id': 1,
            'expert_id': 1,
            'max_points': 100,
            'questions': [{
                'question_text': 'Sample Question',
                'answers': [{'answer_text': 'Sample Answer', 'is_correct': True}]
            }]
        }
        response = self.client.post(reverse('test-add'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


