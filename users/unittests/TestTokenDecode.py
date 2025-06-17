from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class TokenDecodeTests(TestCase):
    """
    Unit tests for token decoding functionality.

        This class contains tests that validate the behavior of the token decoding
        API endpoint. It includes tests for both successful token decoding and handling
        of invalid tokens.

        Methods:
            setUp: Sets up the test environment by initializing the API client, creating
                a test user, and generating an authentication token for the user.
            test_token_decode_success: Tests the successful decoding of a token.
            test_token_decode_invalid_token: Tests the token decoding endpoint with an
                invalid token.

        Attributes:
            None
    """

    def setUp(self):
        """
        Sets up the test environment by initializing the API client, creating a test user,
            and generating an authentication token for the user.

            This method is typically used in unit tests to prepare the necessary components
            for testing API endpoints that require user authentication.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.token = str(RefreshToken.for_user(self.user).access_token)

    def test_token_decode_success(self):
        """
        Tests the successful decoding of a token.

            This method sends a GET request to the API endpoint for token decoding
            and asserts that the response status code is 200, indicating a successful
            request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/token/decode/{self.token}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_decode_invalid_token(self):
        """
        Test the token decoding endpoint with an invalid token.

            This method sends a GET request to the token decoding endpoint using
            an invalid token and asserts that the response status code is
            401 Unauthorized. This verifies that the system correctly handles
            invalid tokens by rejecting them.

            Parameters:
                None

            Returns:
                None
        """
        invalid_token = "invalidtoken"
        response = self.client.get(f"/api/token/decode/{invalid_token}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
