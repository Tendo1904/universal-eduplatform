from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationAPIViewTests(TestCase):
    """
    Tests for the RegistrationAPIView class.
    
        Class Methods:
        - setUp: Sets up the necessary data for testing registration functionality.
        - test_register_user: Tests the functionality of registering a user through the API.
    """

    def setUp(self):
        """
        Sets up the test environment by initializing the client.
        
        Args:
            - self: The object instance
        
        Returns:
            None
        """
        self.client = APIClient()

    def test_register_user(self):
        """
        Test the registration of a new user by sending a POST request to the '/api/register/' endpoint with user data, and then asserting that the user is successfully created.
        
        Parameters:
        - self: The instance of the test case class.
        
        Args:
        - None
        
        Returns:
        None
        """
        data = {'username': 'newuser', 'password': 'newpassword', 'email': 'newuser@example.com'}
        response = self.client.post('/api/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())