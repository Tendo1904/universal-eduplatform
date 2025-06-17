from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..analytics.views import StudentAnalyticsViewSet
from ..analytics.models import StudentAnalytics


class TestStudentAnalyticsViewSet(TestCase):
    """
    A test suite for the StudentAnalyticsViewSet class, responsible for verifying
    the correct functioning of the student analytics API endpoints.

    Methods:
        setUp
        test_retrieve_analytics
        test_calculate_analyticity
        test_create_analytics
        test_update_analytics

    Attributes:
        None

    This class contains tests to validate the retrieval, creation, updating, and
    calculation of student analytics data. Each method interacts with the API
    to ensure that the expected behavior occurs, including correct response
    statuses and appropriate data changes in the database.
    """

    def setUp(self):
        """
        Sets up the test environment for the class.

            This method initializes necessary variables and creates instances
            required for testing, including a student analytics instance and a request factory.

            Parameters:
                None

            Returns:
                None
        """
        self.student_id = 1
        self.test_id = 1
        self.analytics_instance = StudentAnalytics.objects.create(
            student_id=self.student_id
        )
        self.factory = APIRequestFactory()

    def test_retrieve_analytics(self):
        """
        Test the retrieval of student analytics data.

            This method tests the GET request functionality of the
            StudentAnalyticsViewSet to ensure that the analytics data
            for a specific student is correctly retrieved.

            The request is made to the analytics endpoint with the
            specified student ID, and the response status and data
            are asserted to validate correct behavior.

            Parameters:
                None

            Returns:
                None
        """
        view = StudentAnalyticsViewSet.as_view({"get": "retrieve"})
        request = self.factory.get(f"/api/analytics/{self.student_id}/")
        response = view(request, student_id=self.student_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["student_id"], self.student_id)

    def test_calculate_analyticity(self):
        """
        Tests the calculation of analyticity for a student.

            This method simulates a PATCH request to the 'calculate_analyticity' endpoint
            of the StudentAnalyticsViewSet to check if the analyticity for a specific
            student is updated correctly in the database.

            The method prepares a request with student and test IDs, sends it to the view,
            and asserts that the response status code is 200. It also verifies that the
            analyticity for the student has been calculated and is greater than 0.

            Parameters:
                None

            Returns:
                None
        """
        view = StudentAnalyticsViewSet.as_view({"patch": "calculate_analyticity"})
        data = {"student_id": self.student_id, "test_id": self.test_id}
        request = self.factory.patch("/api/analytics/calculate_analyticity/", data=data)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            StudentAnalytics.objects.get(student_id=self.student_id).analyticity > 0,
            True,
        )

    def test_create_analytics(self):
        """
        Test the creation of student analytics.

            This method tests the creation of analytics for a student by
            sending a POST request to the appropriate endpoint and
            verifying that a new record is created in the database.

            Parameters:
                None

            Returns:
                None
        """
        view = StudentAnalyticsViewSet.as_view({"post": "create"})
        data = {"student_id": 2}
        request = self.factory.post("/api/analytics/create/", data=data)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(StudentAnalytics.objects.filter(student_id=2).exists(), True)

    def test_update_analytics(self):
        """
        Tests the update functionality of the Student Analytics API.

            This method simulates an API request to update the analytics data for a specific student and
            verifies that the update is successful by checking the response status code and
            ensuring the data in the database reflects the updated values.

            Parameters:
                None

            Returns:
                None
        """
        view = StudentAnalyticsViewSet.as_view({"put": "update"})
        data = {"student_id": self.student_id, "analyticity": 4, "leadership": 3}
        request = self.factory.put("/api/analytics/update/", data=data)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            StudentAnalytics.objects.get(student_id=self.student_id).analyticity, 4
        )
        self.assertEqual(
            StudentAnalytics.objects.get(student_id=self.student_id).leadership, 3
        )
