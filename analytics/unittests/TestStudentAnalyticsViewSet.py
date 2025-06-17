from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..analytics.views import StudentAnalyticsViewSet
from ..analytics.models import StudentAnalytics


class TestStudentAnalyticsViewSet(TestCase):
    """
    Test suite for the Student Analytics ViewSet.

        This class provides a set of tests to ensure the functionality of the
        Student Analytics API, which handles operations related to student
        analytics, including retrieval, creation, updating, and calculating
        analyticity.

        Methods:
            setUp
            test_retrieve_analytics
            test_calculate_analyticity
            test_create_analytics
            test_update_analytics

        Attributes:
            student_id
            test_id
            analytics_instance
            factory

        Summary:
            - `setUp`: Initializes the test environment and sets up necessary
              attributes for testing.
            - `test_retrieve_analytics`: Tests retrieval of analytics data for a
              specific student.
            - `test_calculate_analyticity`: Tests calculation of analyticity based
              on a student's performance on a test.
            - `test_create_analytics`: Tests the creation of a new analytics entry
              for a student.
            - `test_update_analytics`: Tests the updating of analytics data for a
              specific student.
    """

    def setUp(self):
        """
        Initialize the test environment.

            This method sets up the necessary instance variables for testing,
            including creating a student analytics instance and an API request factory.

            Attributes:
                student_id: The ID of the student being tested.
                test_id: The ID of the test being associated with the student.
                analytics_instance: An instance of StudentAnalytics created with the student_id.
                factory: An instance of APIRequestFactory for simulating API requests.

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
        Test the retrieval of student analytics.

            This method tests the retrieval of analytics data for a specific student
            by sending a GET request to the analytics endpoint and verifies the
            correctness of the response.

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
        Test the calculate analyticity function of the StudentAnalyticsViewSet.

            This method tests the functionality of the endpoint responsible for
            calculating the analyticity of a student's performance on a specific test.

            It sends a PATCH request to the endpoint with the required student and
            test identifiers and verifies that the response status code is 200.
            Additionally, it checks that the analyticity for the specified student
            has been updated and is greater than zero.

            Attributes:
                student_id: The ID of the student whose analyticity is being calculated.
                test_id: The ID of the test associated with the analytics calculation.

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
        Tests the creation of student analytics.

            This method tests the functionality of creating a new student analytics
            entry via a POST request to the specified endpoint. It checks if the
            response status code is 201 and verifies the existence of the newly created
            analytics entry in the database.

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
        Tests the update functionality of the StudentAnalyticsViewSet.

            This method simulates an API PUT request to update the analytics for a specific student.
            It verifies that the response status code is 200 and that the analytics fields are correctly
            updated in the database.

            This method does not take any parameters.

            Returns:
                None: This method does not return any value, but asserts conditions to confirm functionality.
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
