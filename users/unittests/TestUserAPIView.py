from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPIViewTests(TestCase):
    """
    Test cases for the User API views.

        This class contains test cases that validate the access permissions
        for different user roles (admin, teacher, student) to their respective
        API endpoints. It ensures that the expected status codes are received
        when requests are made by users with different access rights.

        Methods:
            setUp
            test_admin_access
            test_teacher_access
            test_student_access

        Attributes:
            None

        Each method sets up the necessary test conditions, performs the API
        requests, and asserts that the responses meet the expected outcomes.
        The `setUp` method prepares the environment needed for the tests,
        while the other methods test access for an admin, teacher, and
        student respectively.
    """

    def setUp(self):
        """
        Sets up the test environment.

            This method initializes the API client and creates user accounts for
            an admin, a teacher, and a student. It also generates access tokens
            for each user, which can be used for authentication in API requests.

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpassword", email="admin@example.com"
        )
        self.teacher_user = User.objects.create_user(
            username="teacher", password="teacherpassword", email="teacher@example.com"
        )
        self.student_user = User.objects.create_user(
            username="student", password="studentpassword", email="student@example.com"
        )
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.teacher_token = RefreshToken.for_user(self.teacher_user).access_token
        self.student_token = RefreshToken.for_user(self.student_user).access_token

    def test_admin_access(self):
        """
        Test access to the admin user endpoint.

            This method verifies that the admin user can successfully access
            the admin user API endpoint and asserts that the response has
            the expected status code.

            Parameters:
                None

            Returns:
                None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")
        response = self.client.get("/api/user/admin/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_access(self):
        """
        Test access for the teacher API endpoint.

            This method simulates a request to the teacher API endpoint
            by using the authorization token of a teacher to verify that
            they have the correct access rights. It checks that the response
            status code is 200 OK, indicating successful access.

            Parameters:
                None

            Returns:
                None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.teacher_token}")
        response = self.client.get("/api/user/teacher/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_access(self):
        """
        Tests access for a student user.

            This method simulates a student user accessing the student-specific
            API endpoint and asserts that the response status code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.student_token}")
        response = self.client.get("/api/user/student/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
