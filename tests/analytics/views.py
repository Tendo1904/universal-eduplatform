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
    A view set for managing student analytics data.

    This class provides endpoints for retrieving, listing, calculating,
    creating, and updating student analytics based on various student
    identifiers and associated metrics.

    Attributes:
        serializer_class: The serializer class used for validating and
                          transforming student analytics data.
        StudentAnalyticsSerializer: The specific serializer implementation
                                     utilized in this view set.

    Methods:
        retrieve: Retrieve student analytics by student ID.
        list: List all student analytics.
        calculate_analyticity: Calculate analyticity for a student.
        calculate_leadership: Calculate leadership for a student and update
                              their analytics.
        create: Create or update student analytics based on the provided
                student ID.
        update: Update student analytics.

    Each method provides distinct functionality for either fetching or
    processing analytics data, allowing seamless interaction with the
    analytics database for students in the system.
    """

    serializer_class = StudentAnalyticsSerializer

    @swagger_auto_schema(
        tags=["Analytics"],
        operation_description="Retrieve student analytics by student ID",
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve student analytics by student ID.

            This method fetches the analytics data for a specific student
            identified by their student ID. The data is serialized and returned
            in the response.

            Args:
                request: The HTTP request object.
                *args: Any additional positional arguments.
                **kwargs: A dictionary of keyword arguments, which must include
                          'student_id' to identify the student whose analytics
                          are to be retrieved.

            Returns:
                A Response object containing the serialized student analytics data
                and an HTTP 200 OK status.
        """
        queryset = StudentAnalytics.objects.filter(student_id=kwargs["student_id"])
        serializer = StudentAnalyticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Analytics"], operation_description="List all student analytics"
    )
    def list(self, *args, **kwargs):
        """
        List all student analytics.

            This method retrieves all student analytics from the database and returns them as a response.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Response: A response object containing a list of all student analytics.
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
        Calculate analyticity for a student.

            This method processes a request containing a student's ID and test ID,
            validates the input data, computes the analyticity for the specified
            student and test, and updates or creates the corresponding record
            in the database.

            Args:
                request: The HTTP request containing data for student ID and test ID.

            Returns:
                A Response object with a message indicating success and an HTTP status code.
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
        Calculate leadership for a student and update their analytics.

            This method processes the incoming request to extract the student ID,
            calculates the leadership score for that student, and then updates or
            creates an entry in the StudentAnalytics database.

            Args:
                request: The incoming HTTP request object containing student information.

            Returns:
                Response: A response object indicating the success of the operation,
                          along with a success message.
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

            This method accepts a request containing a student ID and updates
            or creates an entry in the StudentAnalytics database. If the student ID
            already exists, it updates the record with default values for
            analyticity and leadership.

            Args:
                request: The HTTP request object containing the data for the
                         student ID in the request body.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                Response: A response object indicating the result of the operation
                          with a success message and HTTP status code 201.
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

            This method processes an incoming request to update the analytics data
            for a specific student identified by their student ID. It retrieves the
            existing analytics record, updates it with the new data provided in the request,
            and returns the updated data or errors as appropriate.

            Args:
                request: The HTTP request object containing the student ID and
                         updated analytics data in its payload.

            Returns:
                A Response object containing the updated student analytics data
                if the update is successful, or an error message if the update fails.
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
