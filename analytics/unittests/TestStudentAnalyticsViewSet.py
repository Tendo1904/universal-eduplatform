from django.test import TestCase
from rest_framework.test import APIRequestFactory
from ..analytics.views import StudentAnalyticsViewSet
from ..analytics.models import StudentAnalytics


class TestStudentAnalyticsViewSet(TestCase):
    """
    Class for handling student analytics data in a view set for testing purposes.
    
        Class Methods:
        - setUp: None
        - test_retrieve_analytics: None
        - test_calculate_analyticity: None
        - test_create_analytics: None
        - test_update_analytics: None
    """


    def setUp(self):
        """
        Set up the initial configuration for the test case by initializing student_id, test_id, analytics_instance, and factory.
            
        Parameters:
            - self: the instance of the class
        
        Args:
            None
            
        Returns:
            None
        """
        self.student_id = 1
        self.test_id = 1
        self.analytics_instance = StudentAnalytics.objects.create(student_id=self.student_id)
        self.factory = APIRequestFactory()

    def test_retrieve_analytics(self):
        """
        Performs a unit test to retrieve analytics for a specific student.
                
                Parameters:
                - self: The instance of the class.
                - factory: A factory object to create requests for testing.
                
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
        Test the calculate_analyticity method of the StudentAnalyticsViewSet within the AI module of Universal EduPlatform.
        
        Parameters:
        - self: the instance of the TestStudentAnalyticsViewSet class.
        
        Args:
        - None
        
        Return:
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
        Creates an analytics record for a student with the given student ID.
        
        Args:
            - self: The instance of the class.
        
        Returns:
            None
        """
        view = StudentAnalyticsViewSet.as_view({'post': 'create'})
        data = {'student_id': 2}
        request = self.factory.post('/api/analytics/create/', data=data)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(StudentAnalytics.objects.filter(student_id=2).exists(), True)

    def test_update_analytics(self):
        """
        Performs a test to update student analytics using the StudentAnalyticsViewSet for the specified student ID with new analyticity and leadership values.
        
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