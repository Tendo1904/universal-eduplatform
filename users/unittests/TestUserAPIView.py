from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class UserAPIViewTests(TestCase):
    """
    Class to test the User API views.
    
        Attributes:
        - user (User): The user object used for testing APIs.
        - admin (User): The admin user object used for testing admin access.
        - teacher (User): The teacher user object used for testing teacher access.
        - student (User): The student user object used for testing student access.
        - client (APIClient): The client object to simulate API requests.
    """

    def setUp(self):
        """
        Set up initial data for testing environment.
        
        Parameters:
        - self: The instance of the test case.
        
        Class Fields initialized:
        - client: An instance of APIClient for making API requests.
        - admin_user: The admin user object created with superuser permissions.
        - teacher_user: The teacher user object created with normal user permissions.
        - student_user: The student user object created with normal user permissions.
        - admin_token: Access token for the admin user.
        - teacher_token: Access token for the teacher user.
        - student_token: Access token for the student user.
        
        Returns:
        None
        """
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpassword',
                                                        email='admin@example.com')
        self.teacher_user = User.objects.create_user(username='teacher', password='teacherpassword',
                                                     email='teacher@example.com')
        self.student_user = User.objects.create_user(username='student', password='studentpassword',
                                                     email='student@example.com')
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token
        self.teacher_token = RefreshToken.for_user(self.teacher_user).access_token
        self.student_token = RefreshToken.for_user(self.student_user).access_token

    def test_admin_access(self):
        """
        Test the admin access by making a GET request to the '/api/user/admin/' endpoint using admin credentials.
        
        Parameters:
        - self: the instance of the test case.
        
        Returns:
        None
        
        Args:
        - self: the instance of the test case.
        
        Returns:
        None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/user/admin/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_teacher_access(self):
        """
        A helper method to test teacher access in the API.
            
        Parameters:
        - self: The object instance.
            
        Args:
        - None
            
        Returns:
        - None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.teacher_token}')
        response = self.client.get('/api/user/teacher/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_access(self):
        """
        Performs a test to check access for a student user by making an HTTP GET request to retrieve student information.
        
        Args:
            - self: instance of the class for accessing class attributes and methods.
        
        Returns:
            - None
        """
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.student_token}')
        response = self.client.get('/api/user/student/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)