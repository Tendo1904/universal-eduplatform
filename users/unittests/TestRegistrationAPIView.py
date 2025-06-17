from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationAPIViewTests(TestCase):
    """
    Tests the API functionality for user registration.

    This class contains tests to ensure that the registration API
    behaves as expected, including the ability to register new users
    and validate their data.

    Methods:
        setUp
        test_register_user

    Attributes:
        None

    The methods provide the setup for tests and execute the user registration
    test case, verifying the correct responses and database updates during
    the registration process.
    """

    def setUp(self):
        """
        Initializes the API client.

            This method sets up the API client used for making requests
            during the tests. It is typically called before each test case
            is executed to ensure that the client is in a clean and ready
            state.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()

    def test_register_user(self):
        """
        Tests the registration of a new user.

            This method simulates the registration process for a new user by sending
            a POST request to the registration endpoint with user details. It then
            asserts that the response status code is 201 (Created) and checks that
            the user has been successfully added to the database.

            Parameters:
                None

            Returns:
                None
        """
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post("/api/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())
