from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class SubjectViewTests(TestCase):
    """
    Test suite for the API endpoints related to subjects.

    This class contains tests for listing, retrieving, adding, and
    deleting subjects in the API. It ensures that the API behaves
    as expected for these operations.

    Methods:
        setUp
        test_list_subjects
        test_retrieve_subject
        test_add_subject
        test_delete_subject

    Attributes:
        None

    The methods in this class are designed to verify the correct
    functionality of the subject-related endpoints. The `setUp` method
    initializes the test environment, while the other methods test the
    core API functionality: listing subjects, retrieving a specific
    subject by ID, adding a new subject, and deleting an existing subject.
    Each method checks the response status codes to ensure the API is
    returning the expected results.
    """

    def setUp(self):
        """
        Sets up the test environment for the API client and creates a default subject.

            This method initializes the API client and creates a default subject
            for the tests to use, specifically a subject named "Mathematics".

            Parameters:
                None

            Returns:
                None
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")

    def test_list_subjects(self):
        """
        Test the API endpoint for listing subjects.

            This method sends a GET request to the '/api/subjects/' endpoint
            and verifies that the response status code is 200, indicating a
            successful request.

            Returns:
                None: This method does not return a value, but asserts that
                the status code of the response is 200.
        """
        response = self.client.get("/api/subjects/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_subject(self):
        """
        Test retrieval of a subject from the API.

            This method sends a GET request to the API to retrieve a specific subject
            using its ID and asserts that the response status code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/subjects/{self.subject.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_subject(self):
        """
        Tests the addition of a new subject.

            This method simulates a POST request to the API endpoint for adding a new
            subject and verifies that the response status code indicates successful
            creation.

            The method sends a predefined dictionary containing the subject name
            to the server and checks that the server responds with a status code
            indicating that the subject was successfully created.

            Returns:
                None: This method does not return a value.
        """
        data = {"name": "Physics"}
        response = self.client.post("/api/subjects/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_subject(self):
        """
        Test the deletion of a subject.

            This method sends a DELETE request to the API endpoint for deleting a subject
            and asserts that the response status code is 201 Created, indicating that the
            deletion request was successful.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.delete(f"/api/subjects/delete/{self.subject.id}/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
