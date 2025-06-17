import requests
import unittest


class TestStudentAnalyticsAPI(unittest.TestCase):
    """
    A class to test the Student Analytics API.

    This class contains methods to validate the functionality of various
    endpoints related to student analytics, including retrieval, listing,
    creation, updating, and specific calculations of analytics for students.

    Attributes:
        base_url: The base URL for the Student Analytics API.

    Methods:
        test_retrieve_student_analytics: Tests the retrieval of student analytics.
        test_list_student_analytics: Tests the student analytics listing endpoint.
        test_create_student_analytics: Tests the creation of student analytics.
        test_update_student_analytics: Tests the update functionality for student analytics.
        test_calculate_analyticity: Tests the calculate analyticity API endpoint.
        test_calculate_leadership: Tests the calculation of leadership analytics for a student.
    """

    base_url = "http://127.0.0.1:8000/api/"

    def test_retrieve_student_analytics(self):
        """
        Test the retrieval of student analytics.

            This method sends a GET request to the analytics endpoint for a specific
            student identified by their ID and asserts that the response status
            code is 200, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        student_id = 1
        url = f"{self.base_url}analytics/{student_id}/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_student_analytics(self):
        """
        Tests the student analytics listing endpoint.

            This method sends a GET request to the analytics listing URL and asserts
            that the response status code is 200 (OK), indicating that the request was
            successful.

            Parameters:
                None

            Returns:
                None
        """
        url = f"{self.base_url}analytics/list/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_student_analytics(self):
        """
        Tests the creation of student analytics.

            This method sends a POST request to create student analytics
            using a predefined student ID and asserts that the response's
            status code is 201, indicating successful creation.

            Parameters:
                None

            Returns:
                None
        """
        data = {"student_id": 1}
        url = f"{self.base_url}analytics/create/"
        response = requests.post(url, json=data)
        self.assertEqual(response.status_code, 201)

    def test_update_student_analytics(self):
        """
        Tests the update functionality for student analytics.

            This method sends a PUT request to update the analytics for a specific student.
            It verifies that the server responds with a status code indicating a successful operation.

            Parameters:
                None

            Returns:
                None
        """
        data = {"student_id": 1, "analyticity": 3, "leadership": 4}
        url = f"{self.base_url}analytics/update/"
        response = requests.put(url, json=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_analyticity(self):
        """
        Test the calculate analyticity API endpoint.

            This method sends a PATCH request to the calculate analyticity
            API endpoint with a sample payload and asserts that the response
            status code is 200, indicating a successful operation.

            Parameters:
                None

            Returns:
                None
        """
        data = {"student_id": 2, "test_id": 2}
        url = f"{self.base_url}analytics/calculate_analyticity/"
        response = requests.patch(url, json=data)
        self.assertEqual(response.status_code, 200)

    def test_calculate_leadership(self):
        """
        Test the calculation of leadership analytics for a student.

            This method sends a PATCH request to the leadership calculation endpoint
            with a predefined student ID and asserts that the response status code
            is 200, indicating a successful request.

            Parameters:
                None

            Returns:
                None
        """
        data = {"student_id": 1}
        url = f"{self.base_url}analytics/calculate_leadership/"
        response = requests.patch(url, json=data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
