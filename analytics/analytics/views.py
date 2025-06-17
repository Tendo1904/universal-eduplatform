from rest_framework import status, generics, viewsets
from .models import StudentAnalytics
from .serializers import (
    StudentAnalyticsSerializer,
    StudentIdSerializer,
    StudentIdTestSerializer,
)
from .calculations import calculate_analyticity, calculate_leadership
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class StudentAnalyticsViewSet(viewsets.ViewSet):
    """
    ViewSet for managing student analytics.

    This class provides endpoints to retrieve, create, update, and manage
    student analytics data. It handles various metrics related to student
    performance and interactions.

    Attributes:
        serializer_class: The serializer class used to serialize student
                          analytics data.
        StudentAnalyticsSerializer: The serializer for student analytics
                                    operations.

    Methods:
        retrieve: Retrieve student analytics based on the provided student ID.
        list: Lists all student analytics.
        calculate_analyticity: Calculate analyticity for a student and
                               update their record.
        calculate_leadership: Calculate leadership metrics for a specific
                              student.
        create: Create or update student analytics based on the provided
                student ID.
        update: Update student analytics.

    Class methods provide functionalities such as retrieving analytics
    for a specified student, calculating various metrics, and managing
    the creation and updating of analytics records.
    """

    serializer_class = StudentAnalyticsSerializer

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="Retrieve student analytics by student ID",
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student analytics based on the provided student ID.

            This method retrieves analytics data for a specific student by their ID
            and returns it in a serialized format.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments, including 'student_id' for
                    identifying the student whose analytics data is to be retrieved.

            Returns:
                A Response object containing the serialized analytics data and an HTTP
                status code indicating the result of the operation.
        """
        queryset = StudentAnalytics.objects.filter(student_id=kwargs["student_id"])
        serializer = StudentAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Analytics"], operation_description="List all student analytics"
    )
    def list(self, *args, **kwargs):
        """
        Lists all student analytics.

            This method retrieves all student analytics from the database and returns
            them in a response format.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                A Response object containing a list of student analytics.
        """
        data = list(StudentAnalytics.objects.all().values())
        return Response(data)

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="Calculate analyticity for a student",
        request_body=StudentIdTestSerializer,
    )
    def calculate_analyticity(self, request):
        """
        Calculate analyticity for a student and update their record.

            This method processes the request data to retrieve the student ID
            and test ID, calculates the analyticity for the specified student,
            and updates or creates the corresponding entry in the database
            with the calculated value.

            Args:
                request: The HTTP request object containing the data with
                         'student_id' and 'test_id'.

            Returns:
                Response: A Django REST Framework Response object containing
                          a message indicating the result of the operation
                          and the HTTP status code.
        """
        serializer = StudentIdTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data["student_id"]
        test_id = serializer.validated_data["test_id"]

        analyticity = calculate_analyticity(student_id, test_id)

        StudentAnalytics.objects.update_or_create(
            student_id=student_id, defaults={"analyticity": analyticity}
        )

        return Response({"message": "Added Successfully"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="Calculate leadership for a student",
        request_body=StudentIdSerializer,
    )
    def calculate_leadership(self, request):
        """
        Calculate leadership metrics for a specific student.

            This method processes a request containing a student ID, calculates the leadership
            score for the student, and updates or creates an entry in the StudentAnalytics
            database with the calculated leadership value.

            Args:
                request: The HTTP request object that contains the student ID in its data.

            Returns:
                Response: A response object indicating the success of the operation with a
                message confirming the addition of the leadership score.
        """
        serializer = StudentIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data["student_id"]

        leadership = calculate_leadership(student_id)

        StudentAnalytics.objects.update_or_create(
            student_id=student_id, defaults={"leadership": leadership}
        )

        return Response({"message": "Added Successfully"}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="add student's result",
        request_body=StudentIdSerializer,
    )
    def create(self, request, *args, **kwargs):
        """
        Create or update student analytics based on the provided student ID.

            This method validates the incoming request data containing a student ID,
            and creates a new student analytics record or updates an existing one
            to initialize it with default values for analyticity and leadership.

            Args:
                request: The HTTP request object containing the student ID in the
                         request body.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing a success message and an HTTP status of
                201 Created.
        """
        serializer = StudentIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_id = serializer.validated_data["student_id"]

        StudentAnalytics.objects.update_or_create(
            student_id=student_id, defaults={"analyticity": 0, "leadership": 0}
        )

        return Response(
            {"message": "Created Successfully"}, status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="Update student analytics",
        request_body=StudentAnalyticsSerializer,
    )
    def update(self, request):
        """
        Update student analytics.

            This method updates the analytics information for a specific student identified
            by the student ID provided in the request data. If the student analytics instance
            is found, it is updated with the new data. If the student is not found, a
            NotFound error is raised. The method returns the updated analytics data or
            validation errors if the update fails.

            Args:
                request: The incoming HTTP request containing the data to update the student
                         analytics, which includes the student ID and the new analytics
                         information.

            Returns:
                A Response object containing the updated student analytics data with a status
                of 200 OK, or validation errors with a status of 400 BAD REQUEST.
        """
        data = request.data
        student_id = data["student_id"]
        student_analytics_instance = StudentAnalytics.objects.filter(
            student_id=student_id
        ).first()
        if not student_analytics_instance:
            raise NotFound(detail="Student not found")

        serializer = StudentAnalyticsSerializer(
            instance=student_analytics_instance, data=data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
