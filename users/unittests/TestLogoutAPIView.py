from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutAPIViewTests(TestCase):
    """
    Tests for the LogoutAPIView class.
    
        Class Methods:
        - setUp: Sets up the necessary objects for testing.
        - test_logout: Tests the logout functionality of the LogoutAPIView class.
    """

    def setUp(self):
        """
        Sets up necessary objects and data for testing.
        
        Parameters:
        - self: Instance of the test case.
        
        Initializes the following class fields:
        - client: An instance of APIClient for making API requests.
        - user: A User instance created with specified username, password, and email.
        - token: Access token generated for the user.
        
        Returns:
        - None
        
        Args:
        - self: Instance of the test case.
        
        Return:
        - None
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = RefreshToken.for_user(self.user).access_token

    def test_logout(self):
        """
        Performs a test to log out a user by sending a POST request to the logout endpoint.
        
        Parameters:
            self: The instance of the test class.
            
        Args:
            self: Instance of the test class.
        
        Returns:
            None
        Returns:
            None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post('/api/logout/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)