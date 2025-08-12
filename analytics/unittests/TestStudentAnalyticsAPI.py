import requests
import unittest


class TestStudentAnalyticsAPI(unittest.TestCase):
    """
    This class provides functionalities to analyze student analytics data.
    
        Class Attributes:
        - api_key: The API key used for authentication.
    
        Class Methods:
        - retrieve_student_analytics: Retrieves student analytics data from the API.
        - list_student_analytics: Lists all student analytics data available.
        - create_student_analytics: Creates a new student analytics entry.
        - update_student_analytics: Updates an existing student analytics entry.
        - calculate_analyticity: Calculates the level of analyticity for a given student.
        - calculate_leadership: Calculates the leadership score for a student.
    """

    base_url = 'http://127.0.0.1:8000/api/'

    def test_retrieve_student_analytics(self):
        """
        Retrieves analytics data for a specific student using the provided student ID for the request.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        None
        """
        student_id = 1
        url = f'{self.base_url}analytics/{student_id}/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_student_analytics(self):
        """
        Performs a test to list student analytics by sending a GET request to the analytics list endpoint. Verifies that the response status code is 200.
        
        Parameters:
            self: The instance of the class.
        
        Args:
            None
        
        Returns:
            None
        """
        url = f'{self.base_url}analytics/list/'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_student_analytics(self):
        """
        Creates student analytics by sending a POST request to the analytics endpoint with student_id as data.
        
        Parameters:
        - self: The instance of the class.
        
        Args:
        None
        
        Returns:
        None
        """
        data = {'student_id': 1}
        url = f'{self.base_url}analytics/create/'
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_student_analytics(self):
        """
        Updates the analytics data for a specific student.
                
                - Parameters:
                    - self: The class instance.
                
                - Args:
                    None
                
                - Returns:
                    None
        """
        data = {'student_id': 1, 'analyticity': 3, 'leadership': 4}
        url = f'{self.base_url}analytics/update/'
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_analyticity(self):
        """
        Calculates analyticity for a student based on the given student and test IDs.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        None
        """
        data = {'student_id': 2, 'test_id': 2}
        url = f'{self.base_url}analytics/calculate_analyticity/'
        response = requests.patch(url, json=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_leadership(self):
        """
        Calculate leadership for a student by sending a PATCH request to the analytics endpoint with student_id data.
        
        Args:
        - self: instance of the class
        
        Returns:
        None
        """
        data = {'student_id': 1}
        url = f'{self.base_url}analytics/calculate_leadership/'
        response = requests.patch(url, json=data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
