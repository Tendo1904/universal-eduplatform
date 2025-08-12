from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class SubjectViewTests(TestCase):
    """
    Class for testing views related to subjects in a web application.
    
        Class Methods:
        - setUp: Sets up the necessary data for the tests.
        - test_list_subjects: Tests the functionality to retrieve a list of subjects.
        - test_retrieve_subject: Tests the functionality to retrieve a single subject.
        - test_add_subject: Tests the functionality to add a new subject.
        - test_delete_subject: Tests the functionality to delete a subject.
        Attributes:
        - user: The user instance used for testing subject views.
        - subject: The subject instance used for testing subject views.
    """

    def setUp(self):
        """
        Set up method for initializing necessary objects for tests.
        
        Args:
            self: Instance of the test case class.
        
        Initialized Class Fields:
            - client: APIClient object for interacting with APIs.
            - subject: Subject object representing a subject with the name "Mathematics".
        
        Returns:
            None
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")

    def test_list_subjects(self):
        """
        Summary:
            Test the endpoint '/api/subjects/' by sending a GET request and checking the response status code.
        
        Parameters:
            - self: the instance of the class
        
        Args:
            self (SubjectViewTests): An instance of the SubjectViewTests class.
        
        Returns:
            This method does not return any value.
        """
        response = self.client.get('/api/subjects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_subject(self):
        """
        Summary:
            Retrieves a subject using the provided subject ID and asserts that the response status code is HTTP 200 OK.
        
        Parameters:
            self: The instance of the class.
        
        Args:
            None
        
        Returns:
            None
        """
        response = self.client.get(f'/api/subjects/{self.subject.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_subject(self):
        """
        Adds a new subject by sending a POST request to the '/api/subjects/add/' endpoint with the provided data.
        
        Parameters:
        - self: The instance of the class.
        
        Args:
        - data (dict): A dictionary containing the data for the new subject to be added.
        
        Returns:
        None
        """
        data = {'name': 'Physics'}
        response = self.client.post('/api/subjects/add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_subject(self):
        """
        Deletes a subject using the subject ID and asserts the HTTP response status code to be 201_CREATED.
                
                Parameters:
                - self: The instance of the class.
                
                Returns:
                None
        """
        response = self.client.delete(f'/api/subjects/delete/{self.subject.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
