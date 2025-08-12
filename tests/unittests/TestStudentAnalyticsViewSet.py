from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..analytics.views import StudentAnalyticsViewSet
from ..analytics.models import StudentAnalytics


class TestStudentAnalyticsViewSet(TestCase):
    """
    Class TestStudentAnalyticsViewSet:
        This class provides unit tests for the StudentAnalyticsViewSet class to ensure correct functionality and accuracy of analytics calculations.
    
        Class Methods:
        - setUp: None
        - test_retrieve_analytics: None
        - test_calculate_analyticity: None
        - test_create_analytics: None
        - test_update_analytics: None
    """


    def setUp(self):
        """
        Set up initial data for running tests.
        
        Parameters: 
        - self: the instance of the class.
        
        Initializes the following class fields:
        - student_id: integer representing the student ID.
        - test_id: integer representing the test ID.
        - analytics_instance: an instance of StudentAnalytics created with the provided student ID.
        - factory: an instance of APIRequestFactory.
        
        Args:
        - None
        
        Returns:
        None
        """
        self.student_id = 1
        self.test_id = 1
        self.analytics_instance = StudentAnalytics.objects.create(student_id=self.student_id)
        self.factory = APIRequestFactory()

    def test_retrieve_analytics(self):
        """
        Test the retrieval of analytics for a specific student.
            
            Parameters:
            - self: The instance of the class.
            - student_id: ID of the student for whom analytics are being retrieved.
            
            Returns:
            None
        """
        view = StudentAnalyticsViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'/api/analytics/{self.student_id}/')
        response = view(request, student_id=self.student_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['student_id'], self.student_id)

    def test_calculate_analyticity(self):
        """
        Calculates the analyticity score for a student based on their test results.
        
        Parameters:
        - self: The instance of the class.
        
        Return:
        None
        
        Args:
        - None
        
        Returns:
        - None
        """
        view = StudentAnalyticsViewSet.as_view({'patch': 'calculate_analyticity'})
        data = {'student_id': self.student_id, 'test_id': self.test_id}
        request = self.factory.patch('/api/analytics/calculate_analyticity/', data=data)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudentAnalytics.objects.get(student_id=self.student_id).analyticity > 0, True)

    def test_create_analytics(self):
        """
        This method tests the creation of a student analytics record by sending a POST request to the 'create' endpoint of the StudentAnalyticsViewSet.
        
        Parameters:
        - self: Instance of the class calling the method.
        
        Args:
        None.
        
        Returns:
        None. Performs assertions to verify the successful creation of a student analytics record and checks if the record with the student_id exists in the database.
        """
        view = StudentAnalyticsViewSet.as_view({'post': 'create'})
        data = {'student_id': 2}
        request = self.factory.post('/api/analytics/create/', data=data)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(StudentAnalytics.objects.filter(student_id=2).exists(), True)

    def test_update_analytics(self):
        """
        Updates the analytics data for a student in the database.
        
        Args:
        - self: The instance of the class.
        
        Returns:
        None
        """
        view = StudentAnalyticsViewSet.as_view({'put': 'update'})
        data = {'student_id': self.student_id, 'analyticity': 4, 'leadership': 3}
        request = self.factory.put('/api/analytics/update/', data=data)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(StudentAnalytics.objects.get(student_id=self.student_id).analyticity, 4)
        self.assertEqual(StudentAnalytics.objects.get(student_id=self.student_id).leadership, 3)