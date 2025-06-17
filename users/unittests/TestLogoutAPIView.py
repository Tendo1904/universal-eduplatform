from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutAPIViewTests(TestCase):
    """
    Tests the logout functionality of the API.

    This class contains tests to verify the behavior of the logout endpoint
    in the API. It sets up the necessary environment for testing, including
    user authentication details, and ensures that logout requests are handled
    correctly.

    Methods:
        setUp
        test_logout

    Attributes:
        None

    The `setUp` method prepares the test environment by creating a test user
    and generating an access token for authentication. The `test_logout`
    method checks that a POST request to the logout endpoint functions as
    expected and returns a successful status code.
    """

    def setUp(self):
        """
        Set up the test environment.

            This method initializes the test client and creates a test user with a specified
            username, password, and email address. It also generates an access token for the
            created user, which can be used for authentication in subsequent tests.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@example.com"
        )
        self.token = RefreshToken.for_user(self.user).access_token

    def test_logout(self):
        """
        Tests the logout functionality of the API.

            This method simulates a logout request by sending a POST request
            to the logout endpoint after setting the appropriate authorization
            credentials. It then asserts that the response returns a status
            code indicating a successful logout.

            Parameters:
                None

            Returns:
                None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")
        response = self.client.post("/api/logout/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
