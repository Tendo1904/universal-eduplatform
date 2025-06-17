from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class ThemeViewTests(TestCase):
    """
    Test suite for the Theme API endpoints.

        This class contains tests that verify the functionality of the Theme
        API, including listing, retrieving, adding, and deleting themes.

        Methods:
            setUp
            test_list_themes
            test_retrieve_theme
            test_add_theme
            test_delete_theme
            test_get_by_subject_id

        Attributes:
            client
            subject
            theme

        The methods in this class set up the necessary environment for testing
        the Theme API, ensuring that the client is ready and that a subject
        and theme are created for the tests. The tests themselves check
        various aspects of the API's functionality, from listing themes to
        ensuring proper handling of theme addition and deletion.
    """

    def setUp(self):
        """
        Sets up the test environment by initializing the API client and creating
            a subject and theme for testing.

            This method is typically used in testing scenarios to prepare the necessary
            context and objects before running test cases.

            Attributes:
                client: An instance of the APIClient used for making API requests during
                        tests.
                subject: A Subject object representing a subject created with the name
                         "Mathematics".
                theme: A Theme object representing a theme created with the name "Algebra"
                       associated with the specified subject.

            Returns:
                None: This method does not return any value.
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")
        self.theme = Theme.objects.create(name="Algebra", id_subject=self.subject)

    def test_list_themes(self):
        """
        Tests the API endpoint for listing themes.

            This method sends a GET request to the '/api/themes/' endpoint and
            asserts that the response status code is 200 OK, indicating that
            the themes list was retrieved successfully.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get("/api/themes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_theme(self):
        """
        Test the retrieval of a theme by its ID.

            This method sends a GET request to the API endpoint for a specific theme and verifies that
            the response status code is 200, indicating success.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/themes/{self.theme.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_theme(self):
        """
        Tests the addition of a new theme via the API.

            This method sends a POST request to the '/api/themes/add/' endpoint with
            a predefined theme data payload and checks if the response
            indicates successful creation of the theme.

            Parameters:
                None

            Returns:
                None
        """
        data = {"name": "Geometry", "id_subject": self.subject.id}
        response = self.client.post("/api/themes/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_theme(self):
        """
        Tests the DELETE endpoint for removing a theme.

            This method sends a DELETE request to the API endpoint responsible for
            deleting a theme identified by its ID. It asserts that the response
            status code is 201, indicating the request was successfully processed.

            Parameters:
              None

            Returns:
              None
        """
        response = self.client.delete(f"/api/themes/delete/{self.theme.id}/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_by_subject_id(self):
        """
        Test retrieval of a theme by its subject ID.

            This method sends a GET request to the API to retrieve a theme
            associated with a specific subject ID and verifies that the
            response status code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/themes/subject/{self.subject.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
