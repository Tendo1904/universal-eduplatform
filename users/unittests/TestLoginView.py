from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class LoginViewTests(TestCase):
    """
    This class contains unit tests for the LoginView class. 
    
        Class Methods:
        - setUp: None
        - test_login_success: None
        - test_login_invalid_credentials: None
        - test_login_inactive_user: None
    """

    def setUp(self):
        """
        Set up test data by creating a test API client and a test user.
        
        Parameters:
        - self: The instance of the test case.
        
        Fields initialized:
        - client: An instance of APIClient for making API requests.
        - user: An instance of the User model representing a test user.
        
        Returns:
        None
        
        Args:
        - username (str): The username for the test user.
        - password (str): The password for the test user.
        - email (str): The email address for the test user.
        - is_active (bool): A boolean value indicating whether the test user is active or not.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com',
                                             is_active=True)

    def test_login_success(self):
        """
        Test the successful login functionality.
        
        Args:
            self: The instance of the test case.
        
        Returns:
            None
        """
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.cookies)
        self.assertIn('refresh_token', response.cookies)

    def test_login_invalid_credentials(self):
        """
        Performs a test to verify login with invalid credentials by sending a POST request with wrong username and password to the '/api/login/' endpoint. It then asserts that the response status code is HTTP 404 NOT FOUND.
            
        Args:
        - self: Instance of the test case class.
        
        Returns:
        None
        """
        data = {'username': 'wronguser', 'password': 'wrongpassword'}
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_inactive_user(self):
        """
        A method to test the login functionality for an inactive user by sending a POST request to the login API endpoint with the credentials of an inactive user.
                
                Parameters:
                - self: the instance of the test case class.
                
                Returns:
                None
                - None
                
                < triple_quotes>
        """
        self.user.is_active = False
        self.user.save()
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/api/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
