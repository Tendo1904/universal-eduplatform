from rest_framework import status, generics, viewsets
from .models import StudentAnalytics
from .serializers import StudentAnalyticsSerializer, StudentIdSerializer, StudentIdTestSerializer
from .calculations import calculate_analyticity, calculate_leadership
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class StudentAnalyticsViewSet(viewsets.ViewSet):
    """
    Class representing a view set for performing analytics on student data.
    
        Class Methods:
        - retrieve: Get a single student analytics record.
        - list: Get a list of student analytics records.
        - calculate_analyticity: Calculate the analyticity score for a student.
        - calculate_leadership: Calculate the leadership score for a student.
        - create: Create a new student analytics record.
        - update: Update an existing student analytics record.
    
        Class Attributes:
        - serializer_class: The serializer class used for serializing/deserializing student analytics data.
        - StudentAnalyticsSerializer: The serializer for student analytics data.
    """

    serializer_class = StudentAnalyticsSerializer

    @swagger_auto_schema(tags=["Analytics"], operation_description="Retrieve student analytics by student ID")
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student analytics by student ID.
        
        Args:
        - request: The request object.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments.
        - kwargs['student_id']: The ID of the student for whom analytics data is retrieved.
        
        Returns:
        - Response: A Response object containing student analytics data for the specified student ID.
        """
        queryset = StudentAnalytics.objects.filter(student_id=kwargs['student_id'])
        serializer = StudentAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=["Analytics"], operation_description="List all student analytics")
    def list(self, *args, **kwargs):
        """
        Retrieves all student analytics data from the database.
        
        Args:
            - self: The instance of the class.
        
        Returns:
            - Response: A response with the list of student analytics data.
        """
        data = list(StudentAnalytics.objects.all().values())
        return Response(data)

    @swagger_auto_schema(tags=["Analytics"], operation_description="Calculate analyticity for a student",
                         request_body=StudentIdTestSerializer)
    def calculate_analyticity(self, request):
        """
        Calculate the analyticity value for a student based on the provided student_id and test_id data and update the corresponding StudentAnalytics object.
        
        Parameters:
        - self: The instance of the class.
        - request: The request object containing data for student_id and test_id.
        
        Return:
        - Dict: A dictionary with a success message upon successful addition of analyticity data.
        
        Args:
        - student_id (int): Identifier for the student.
        - test_id (int): Identifier for the test.
        
        Returns:
        - Dict: A dictionary with a success message upon successful addition of analyticity data.
        
        Class Fields Initialized:
        - serializer: Used to serialize the request data.
        - student_id: Identifier for the student.
        - test_id: Identifier for the test.
        - analyticity: Calculated analyticity value.
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
        Calculate leadership for a student based on the provided student ID and update the database with the calculated leadership value.
        
        Args:
            - self: The instance of the class.
            - request: The request object containing student information.
        
        Returns:
            Response: A Response object with a message indicating successful addition.
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
        Creates a new student analytics record using the provided student ID.
        
        Parameters:
        - request: the request object containing the student details.
        
        Args:
        - request (Request): The request object containing the student details.
        
        Returns:
        - Response: Response containing a success message upon successful creation.
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
        Update student analytics based on the provided request data.
        
        Args:
            - self: The reference to the current instance of the class.
            - request: The request object containing data for updating student analytics.
        
        Returns:
            - Response: A response object containing updated student analytics data or errors.
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
