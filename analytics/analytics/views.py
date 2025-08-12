from rest_framework import status, generics, viewsets
from .models import StudentAnalytics
from .serializers import StudentAnalyticsSerializer, StudentIdSerializer, StudentIdTestSerializer
from .calculations import calculate_analyticity, calculate_leadership
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class StudentAnalyticsViewSet(viewsets.ViewSet):
    """
    Class for handling student analytics data in a view set.
    
        Class Attributes:
        - serializer_class: Serializer class for student analytics data.
    
        Class Methods:
        - retrieve: Retrieves a specific student analytics record.
        - list: Lists all student analytics records.
        - calculate_analyticity: Calculates analyticity score for a student.
        - calculate_leadership: Calculates leadership potential for a student.
        - create: Creates a new student analytics record.
        - update: Updates an existing student analytics record.
    """

    serializer_class = StudentAnalyticsSerializer

    @swagger_auto_schema(tags=["Analytics"], operation_description="Retrieve student analytics by student ID")
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student analytics data for the given student ID.
            
            Parameters:
                self: The object instance.
                request: The HTTP request object.
                *args: Additional arguments.
                **kwargs: Additional keyword arguments, 'student_id' is expected.
                
            Return:
                Response: JSON response containing student analytics data for the given student ID.
        """
        queryset = StudentAnalytics.objects.filter(student_id=kwargs['student_id'])
        serializer = StudentAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Analytics"], operation_description="List all student analytics")
    def list(self, *args, **kwargs):
        """
        Retrieves all student analytics data.
        
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            Response: A response object containing the student analytics data.
        """
        data = list(StudentAnalytics.objects.all().values())
        return Response(data)

    @swagger_auto_schema(tags=["Analytics"], operation_description="Calculate analyticity for a student",
                         request_body=StudentIdTestSerializer)
    def calculate_analyticity(self, request):
        """
        Calculate analyticity for a student based on the provided request data.
        
        Args:
        - self: The instance of the class.
        - request: The request object containing student and test details.
        
        Returns:
        - dict: A dictionary response with a message indicating successful addition.
        - Status: HTTP 200 OK
        """
        serializer = StudentIdTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']
        test_id = serializer.validated_data['test_id']

        analyticity = calculate_analyticity(student_id, test_id)

        StudentAnalytics.objects.update_or_create(
            student_id=student_id,
            defaults={'analyticity': analyticity}
        )

        return Response({"message": "Added Successfully"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Analytics"], operation_description="Calculate leadership for a student",
                         request_body=StudentIdSerializer)
    def calculate_leadership(self, request):
        """
        Calculate leadership for a student and update StudentAnalytics with the calculated leadership value.
        
        Args:
            - self: The instance of the class.
            - request: The request object containing student information.
        
        Returns:
            - Response: A dictionary with a success message after adding the student's leadership value.
        """
        serializer = StudentIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']

        leadership = calculate_leadership(student_id)

        StudentAnalytics.objects.update_or_create(
            student_id=student_id,
            defaults={'leadership': leadership}
        )

        return Response({"message": "Added Successfully"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Analytics"], operation_description="add student's result",
                         request_body=StudentIdSerializer)
    def create(self, request, *args, **kwargs):
        """
        Creates a new StudentAnalytics object based on the provided student_id.
        
        Args:
            - request: The HTTP request object containing data to create the StudentAnalytics object.
        
        Returns:
            A Response object indicating the status of the creation process.
        """
        serializer = StudentIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data['student_id']

        StudentAnalytics.objects.update_or_create(
            student_id=student_id,
            defaults={'analyticity': 0, 'leadership': 0}
        )

        return Response({"message": "Created Successfully"}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(tags=["Analytics"], operation_description="Update student analytics",
                         request_body=StudentAnalyticsSerializer)
    def update(self, request):
        """
        Updates student analytics based on the provided request data.
        
        Args:
        - self: The instance of the class.
        - request: The request containing data for updating student analytics.
        
        Returns:
        - Response: A response indicating the result of the update operation.
        """
        data = request.data
        student_id = data['student_id']
        student_analytics_instance = StudentAnalytics.objects.filter(student_id=student_id).first()
        if not student_analytics_instance:
            raise NotFound(detail="Student not found")

        serializer = StudentAnalyticsSerializer(instance=student_analytics_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
