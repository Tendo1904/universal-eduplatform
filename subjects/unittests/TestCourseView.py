from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class CourseViewTests(TestCase):
    """
    Tests for the Course API views.

    This class contains a series of unit tests for the Course API endpoints,
    ensuring that various functionalities such as adding, retrieving,
    listing, and deleting courses work as expected.

    Methods:
        - setUp
        - test_add_course
        - test_retrieve_course
        - test_list_courses
        - test_delete_course
        - test_get_by_subject_id
        - test_get_by_expert_id
        - test_get_expert_info

    Attributes:
        - client
        - subject
        - course

    The methods in this class include setup for the test environment,
    as well as tests that assert the correct behavior of API calls
    related to courses, including their addition, retrieval,
    listing, and deletion. The attributes include the API client
    for making requests, a subject object for context in tests,
    and a course object for testing course-related functionalities.
    """

    def setUp(self):
        """
        Prepare the test environment.

            This method sets up the necessary test fixtures by creating an instance
            of the API client and initializing a subject and a course for testing
            purposes.

            Attributes:
                self.client: An instance of the APIClient used for making requests.
                self.subject: A Subject object created for the purpose of testing.
                self.course: A Course object linked to the subject, created for testing.

            Returns:
                None
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")
        self.course = Course.objects.create(
            name_course="Basic Math",
            id_subject=self.subject,
            description="Basic Math Course",
            id_expert=1,
        )

    def test_add_course(self):
        """
        Tests the addition of a new course.

            This method sends a POST request to the API to add a new course with specified details and asserts
            that the response status code indicates a successful creation.

            Parameters:
                None

            Returns:
                None
        """
        data = {
            "name_course": "Advanced Math",
            "id_subject": self.subject.id,
            "description": "Advanced Math Course",
            "id_expert": 2,
        }
        response = self.client.post("/api/courses/add/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_course(self):
        """
        Tests the retrieval of a course.

            This method sends a GET request to the API endpoint for a specific course
            and asserts that the response status code is 200, indicating the request
            was successful.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/courses/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_courses(self):
        """
        Tests the API endpoint for listing courses.

            This method sends a GET request to the '/api/courses/' endpoint
            and asserts that the response status code is 200, indicating
            a successful request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        """
        Tests the deletion of a course.

            This method sends a DELETE request to the course deletion endpoint
            and asserts that the response status code is 201 Created, indicating
            that the course has been successfully deleted.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.delete(f"/api/courses/delete/{self.course.id}/")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_by_subject_id(self):
        """
        Tests the retrieval of a course by its subject ID.

            Sends a GET request to the specified endpoint to fetch course information
            associated with the given subject ID, and verifies that the response status
            code is 200 OK, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/courses/subject/{self.subject.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_expert_id(self):
        """
        Tests the GET request for retrieving courses by expert ID.

            This method sends a GET request to the API endpoint for retrieving
            courses associated with a specific expert identified by their ID.
            It asserts that the response status code is 200, indicating a successful
            retrieval of the data.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(f"/api/courses/expert/{self.course.id_expert}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expert_info(self):
        """
        Test the retrieval of expert information for a specific course and subject.

            This method sends a GET request to the API endpoint for obtaining
            expert information related to a particular course and subject.
            It asserts that the response status code is 200, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            f"/api/courses/expert/{self.course.id_expert}/subject/{self.subject.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
