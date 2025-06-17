from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User


class LoginViewTests(TestCase):
    """
    Test case for the login view functionality of the application.

    This class contains unit tests to verify the correct behavior
    of the login functionality, including successful login, handling
    of invalid credentials, and attempts to log in with inactive user accounts.

    Methods:
        setUp
        test_login_success
        test_login_invalid_credentials
        test_login_inactive_user

    Attributes:
        None

    Summary:
        - setUp: Initializes the test environment, including test client
          and user setup.
        - test_login_success: Tests the application's response to a valid
          login attempt, expecting a status code of 200 OK.
        - test_login_invalid_credentials: Tests the application's response
          to invalid login credentials, expecting a status code of 404.
        - test_login_inactive_user: Tests the application's response for
          an inactive user login attempt, also expecting a status code of 404.
    """

    def setUp(self):
        """
        Sets up the test environment.

            This method initializes the test client and creates a test user
            with specified credentials. It prepares the necessary conditions
            for running the test cases.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            is_active=True,
        )

    def test_login_success(self):
        """
        Tests the successful login functionality.

            This method simulates a user logging into the application by sending
            a POST request with valid credentials. It checks if the response
            status code is 200 OK and verifies that the relevant cookies for
            authentication are set in the response.

            Parameters:
                None

            Returns:
                None
        """
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/api/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_login_invalid_credentials(self):
        """
        Tests the login functionality with invalid credentials.

            This method sends a login request using incorrect username and password
            to verify that the server responds with a 404 Not Found status code,
            indicating that the login attempt was unsuccessful.

            Parameters:
                None

            Returns:
                None
        """
        data = {"username": "wronguser", "password": "wrongpassword"}
        response = self.client.post("/api/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_inactive_user(self):
        """
        Test the login functionality for an inactive user.

            This method tests that an attempt to log in with an inactive user account
            returns a 404 Not Found response. It first sets the user's status to
            inactive, then makes a post request to the login endpoint with the
            user's credentials and asserts that the response status code is 404.

            Parameters:
                None

            Returns:
                None
        """
        self.user.is_active = False
        self.user.save()
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post("/api/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
