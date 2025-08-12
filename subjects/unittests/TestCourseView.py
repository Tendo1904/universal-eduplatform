from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Subject, Theme, Course


class CourseViewTests(TestCase):
    """
    Class CourseViewTests is a test case class for testing course related views and functionalities.
    
        Class Methods:
        - setUp: None
        - test_add_course: None
        - test_retrieve_course: None
        - test_list_courses: None
        - test_delete_course: None
        - test_get_by_subject_id: None
        - test_get_by_expert_id: None
        - test_get_expert_info: None
    """

    def setUp(self):
        """
        Sets up initial data for tests by creating necessary objects such as client, subject, and course.
        
        Parameters:
        - self: The instance of the class.
        
        Fields Initialized:
        - client: APIClient instance used for making API requests.
        - subject: The created Subject object representing a specific subject with the name "Mathematics".
        - course: The created Course object representing a course named "Basic Math", associated with the subject "Mathematics", 
                 with a description of "Basic Math Course" and linked to an expert with an ID of 1.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        None
        """
        self.client = APIClient()
        self.subject = Subject.objects.create(name="Mathematics")
        self.course = Course.objects.create(name_course="Basic Math", id_subject=self.subject,
                                            description="Basic Math Course", id_expert=1)

    def test_add_course(self):
        """
        Test the addition of a course by sending a POST request to the endpoint '/api/courses/add/' 
        with course data. Verify that the course is created successfully with a status code of 201.
        
        Args:
        - self: The instance of the TestCase class that allows accessing the testing client and other resources.
        
        Return:
        None
        """
        data = {'name_course': 'Advanced Math', 'id_subject': self.subject.id, 'description': 'Advanced Math Course',
                'id_expert': 2}
        response = self.client.post('/api/courses/add/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_course(self):
        """
        Retrieves a course using the provided client and asserts the response status code is 200 OK.
        
        Parameters:
        - self: The instance of the CourseViewTests class.
        
        Returns:
        None
        """
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_courses(self):
        """
        Test the functionality of listing courses via the API.
        
        Args:
        - self: The object instance.
        
        Returns:
        None
        """
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_course(self):
        """
        <triple_quotes>
                Deletes a course using the course ID, asserts the status code of the response, and is a part of managing themes within the project.
                
                Parameters:
                - self: The instance of the class.
                
                Returns:
                None
                <triple_quotes>
        """
        response = self.client.delete(f'/api/courses/delete/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_by_subject_id(self):
        """
        Test method to validate the functionality of retrieving a course by subject ID.
        
        Args:
            self: instance of the test class.
        
        Returns:
            None.
        """
        response = self.client.get(f'/api/courses/subject/{self.subject.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_expert_id(self):
        """
        Retrieve course information by expert ID and assert the response status code.
        
        Parameters:
        - self: The object instance.
        
        Returns:
        None
        
        Args:
        - self: The object instance.
        
        Returns:
        None
        """
        response = self.client.get(f'/api/courses/expert/{self.course.id_expert}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_expert_info(self):
        """
        Performs a unit test to validate the functionality of retrieving expert information for a particular course subject.
        
        Parameters:
        - self: Reference to the current instance of the class.
        
        Returns:
        None
        
        Args:
        - response: The HTTP response object returned from the API call.
        
        Return:
        - None
        """
        response = self.client.get(f'/api/courses/expert/{self.course.id_expert}/subject/{self.subject.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)