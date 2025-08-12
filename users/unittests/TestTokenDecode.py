from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TokenDecodeTests(TestCase):
    """
    This class provides unit tests for the TokenDecode class to validate token decoding functionality.
    
        Class Methods:
        - setUp: Sets up the necessary environment for testing.
        - test_token_decode_success: Tests the TokenDecode class for successful token decoding.
        - test_token_decode_invalid_token: Tests the TokenDecode class for handling invalid tokens.
    """

    def setUp(self):
        """
        Set up necessary data for testing.
        
        Parameters:
        - self: The instance of the class.
        
        Fields initialized:
        - client: An instance of the APIClient class.
        - user: A new User object with provided username, password, and email.
        - token: Access token as a string generated for the user.
        
        Returns:
        None.
        
        Args:
        - self: The instance of the TokenDecodeTests class.
        
        Return:
        None.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_token_decode_success(self):
        """
        Retrieve the decoded information for a given token and assert the response status code is 200.
        
        Args:
        - self: the instance of the test case class.
        
        Return:
        None
        """
        response = self.client.get(f'/api/token/decode/{self.token}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_decode_invalid_token(self):
        """
        Tests the decoding of an invalid token by sending a GET request to the token decode API endpoint with an invalid token.
        
        Parameters:
        - self: The object instance.
        
        Returns:
        None
        
        Args:
        - self: The object instance.
        
        Return:
        None
        """
        invalid_token = 'invalidtoken'
        response = self.client.get(f'/api/token/decode/{invalid_token}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)