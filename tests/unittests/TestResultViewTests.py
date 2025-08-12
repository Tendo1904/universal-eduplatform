from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class ResultsViewTests(TestCase):
    """
    This class contains unit tests for the ResultsView view functions.
    
        Class Methods:
        - setUp: None
        - test_add_result: None
        - test_list_results: None
        - test_get_by_result_id: None
        - test_get_by_student_test_id: None
        - test_get_by_student_id: None
        - test_get_by_test_id: None
        - test_full_student_test_id: None
        - test_full_student_id: None
        - test_full_test_id: None
    
        Attributes:
        - attributes mentioned in the constructor method's docstring
    
        This class tests the functionality of retrieving, adding, and listing results using different criteria such as result ID, student test ID, student ID, and test ID.
    """

    def setUp(self):
        """
        Set up the environment for testing by initializing necessary objects and records in the database.
        
        Args:
            - self: The instance of the test case.
            
        Returns:
            - None
        """
        self.client = APIClient()
        self.test = Test.objects.create(
            author_id=1,
            subject_id=1,
            theme_id=1,
            expert_id=1,
            max_points=100
        )
        self.question = Question.objects.create(id_test=self.test, question_text="Sample Question")
        self.answer = Answer.objects.create(id_question=self.question, answer_text="Sample Answer", is_correct=True)
        self.result = Result.objects.create(id_user=1, id_test=self.test.id, points_user=0)
        self.solution = Solutions.objects.create(id_result=self.result, id_question=self.question,
                                                 id_answer=self.answer)

    def test_add_result(self):
        """
        Adds a test result for a user by posting the result data to a specific endpoint.
        
        Args:
            self: The instance of the class.
            
        Returns:
            None. This method does not return any value.
        """
        data = {
            'id_user': 1,
            'id_test': self.test.id,
            'subject': 'Math',
            'theme': 'Algebra',
            'solutions': [{
                'id_question': self.question.id,
                'id_answer': self.answer.id
            }]
        }
        response = self.client.post(reverse('results-add'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_results(self):
        """
        Performs a test to list results using the client.
        
        Parameters:
            - self: The instance of the class.
        
        Returns:
            None
            
        Args:
            - self: Instance of the ResultsViewTests class.
            
        Return:
            None
        """
        response = self.client.get(reverse('results-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_result_id(self):
        """
        Summary: Retrieve a result by its ID using the 'results-get-by-id' endpoint and perform a unit test to verify the response status code.
        
        Args:
        - self: The instance of the class.
        
        Returns: None
        """
        response = self.client.get(reverse('results-get-by-id', kwargs={'id': self.result.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_student_test_id(self):
        """
        Retrieves test results by student test ID.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        - None
        """
        response = self.client.get(
            reverse('results-get-by-student-test-id', kwargs={'testId': self.test.id, 'studentId': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_student_id(self):
        """
        Performs a test by fetching the results of a student using the student ID.
        
        Parameters:
            - self: The instance of the test case.
        
        Returns:
            None
        
        Args:
            - self: The instance of the test case.
        
        Returns:
            None
        """
        response = self.client.get(reverse('results-get-by-student-id', kwargs={'studentId': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_test_id(self):
        """
        Performs a test to retrieve results by test ID.
        
        Parameters:
        - self: The instance of the class.
        
        Returns:
        None
        
        Args:
        - self: The instance of the ResultsViewTests class.
        
        Returns:
        None
        """
        response = self.client.get(reverse('results-get-by-test-id', kwargs={'testId': self.test.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_student_test_id(self):
        """
        Summary:
            Test the full student test ID by making a GET request to the corresponding endpoint and asserting the response status code.
        
        Parameters:
            self: The instance of the class.
        
        Args:
            None
        
        Returns:
            None
        """
        response = self.client.get(
            reverse('results-full-student-test-id', kwargs={'testId': self.test.id, 'studentId': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_student_id(self):
        """
        Test the endpoint for fetching results using a full student ID.
        
        Args:
            self: The instance of the class.
        
        Return:
        None
        """
        response = self.client.get(reverse('results-full-student-id', kwargs={'studentId': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_test_id(self):
        """
        Performs a test for the full test ID by sending a GET request to retrieve results for a specific test ID.
        
        Parameters:
        - self: The instance of the class.
        
        Returns:
        None
        
        Args:
        - self: The instance of the class.
        
        Return:
        None
        """
        response = self.client.get(reverse('results-full-test-id', kwargs={'testId': self.test.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == '__main__':
    ResultsViewTests()
