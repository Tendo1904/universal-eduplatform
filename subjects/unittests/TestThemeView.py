from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class ThemeViewTests(TestCase):
    """
    A class for testing views related to themes.
    
        Class Methods:
        - setUp: Initializes the test environment.
        - test_list_themes: Tests the functionality to list all themes.
        - test_retrieve_theme: Tests the functionality to retrieve a specific theme.
        - test_add_theme: Tests the functionality to add a new theme.
        - test_delete_theme: Tests the functionality to delete a theme.
        - test_get_by_subject_id: Tests the functionality to get a theme by subject ID.
    """

    def setUp(self):
        """
        Set up initial data for testing purposes.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        None
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")
        self.theme = Theme.objects.create(name="Algebra", id_subject=self.subject)

    def test_list_themes(self):
        """
        Summary:
                    Perform a test to list themes by making a GET request to the '/api/themes/' endpoint and asserting the response's status code is HTTP_200_OK.
                
                Parameters:
                    - self: The instance of the test case.
                
                Returns:
                    None
        """
        response = self.client.get('/api/themes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_theme(self):
        """
        Retrieve a theme object by making a GET request to the API endpoint.
                
                Parameters:
                - self: The instance of the class that invokes the method.
                
                Returns:
                None
        """
        response = self.client.get(f'/api/themes/{self.theme.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_theme(self):
        """
        Adds a new theme for the subject using an HTTP POST request to the API.
        
        Parameters:
        - self: The instance of the class calling this method.
        
        Args:
        - None
        
        Returns:
        - None. The method asserts that the response status code is HTTP_201_CREATED.
        """
        data = {'name': 'Geometry', 'id_subject': self.subject.id}
        response = self.client.post('/api/themes/add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_theme(self):
        """
        Deletes a theme using the API by sending a DELETE request to the specified theme ID endpoint.
        
        Parameters:
            - self: The reference to the instance of the class.
        
        Returns:
            None
        Args:
            - self (ThemeViewTests): An instance of the ThemeViewTests class.
        
        Returns:
            None
        """
        response = self.client.delete(f'/api/themes/delete/{self.theme.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_by_subject_id(self):
        """
        Retrieves a theme by subject ID and asserts the response status code.
                
                Parameters:
                - self: the instance of the ThemeViewTests class.
                
                Returns:
                None
        """
        response = self.client.get(f'/api/themes/subject/{self.subject.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)