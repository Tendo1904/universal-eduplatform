from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import *


class SubjectView(viewsets.ModelViewSet):
    """
    Handles operations related to subjects, including retrieval, addition, and deletion of subject data.

    Attributes:
        queryset: A collection of all Subject instances.
        serializer_class: The serializer class used for converting Subject instances to and from JSON.
        SubjectSerializer: A specific serializer implementation for subjects.

    Methods:
        list: Retrieve and return a list of all subjects.
        retrieve: Retrieve a subject by its primary key.
        add: Adds a new subject based on the provided request data.
        delete: Delete a subject based on the provided primary key.

    Each method has a specific role:
    - `list` fetches all subjects and returns them in JSON format.
    - `retrieve` fetches a single subject by its primary key.
    - `add` creates a new subject using data from the request.
    - `delete` removes a subject based on its primary key, handling success and error responses appropriately.
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieve and return a list of all subjects.

            This method queries the database for all Subject instances and returns
            the results in a response.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing a list of all subjects in JSON format.
        """
        data = list(Subject.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a subject by its primary key.

            This method fetches a subject from the database using the provided primary key (pk)
            and returns the subject data in a response format.

            Args:
                request: The request object containing information about the request.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments containing the primary key (pk) for the subject.

            Returns:
                A Response object containing the subject data retrieved from the database.
        """
        data = list(Subject.objects.filter(id=kwargs["pk"]).values())
        return Response(data)

    def add(self, request, *args, **kwargs):
        """
        Adds a new subject based on the provided request data.

            This method processes the given request data to create and save a new subject.
            If the data is valid, the subject is successfully created and a confirmation message
            is returned with a 201 status code. If the data is invalid, an error message is
            returned with a 400 status code.

            Args:
                request: The request object containing the data to create a new subject.
                *args: Additional positional arguments (not used in this method).
                **kwargs: Additional keyword arguments (not used in this method).

            Returns:
                A Response object containing a message and the HTTP status code.
        """
        subject_serializer_data = SubjectSerializer(data=request.data)
        if subject_serializer_data.is_valid():
            subject_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response(
                {"message": "Added Sucessfully", "status": status_code}, status_code
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "Please fill the datails", "status": status_code},
                status_code,
            )

    def delete(self, request, *args, **kwargs):
        """
        Delete a subject based on the provided primary key.

            This method attempts to delete a subject from the database using the
            primary key specified in the `kwargs`. If the subject is successfully
            deleted, it returns a success message with a created status. If
            the subject does not exist, it returns an error message with a
            bad request status.

            Args:
                request: The HTTP request object containing metadata about the
                    request.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments where 'pk' is expected to be the
                    primary key of the subject to delete.

            Returns:
                A Response object containing a message indicating the result of
                the delete operation and the corresponding HTTP status code.
        """
        subject_data = Subject.objects.filter(id=kwargs["pk"])
        if subject_data:
            subject_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response(
                {"message": "Deleted Sucessfully", "status": status_code}, status_code
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "Data not found", "status": status_code}, status_code
            )


class ThemeView(viewsets.ModelViewSet):
    """
    A view class for managing themes, providing functionalities to
    retrieve, add, and delete themes, as well as fetch themes by
    associated subject IDs.

    Attributes:
        queryset: A query set used to retrieve theme records from the database.
        serializer_class: The serializer class used for validating and
            serializing theme data.
        ThemeSerializer: A specific serializer for theme objects.

    Methods:
        list: Retrieves a list of all themes.
        retrieve: Retrieve a specific theme based on its ID.
        add: Adds a new theme based on provided request data.
        delete: Delete a theme by its ID.
        getBySubjectId: Retrieve themes associated with a specific subject ID.

    Each method handles specific operations related to themes, such as
    retrieving all theme records, getting a theme by ID, adding a new
    theme, deleting a theme, or filtering themes by subject ID.
    """

    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all themes.

            This method queries the database for all theme records and returns them
            in the form of a JSON response.

            Args:
                request: The request object containing request data.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing a list of theme records in JSON format.
        """
        data = list(Theme.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific theme based on its ID.

            This method queries the database for a theme with the given primary key (ID)
            and returns the associated data in the response.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments, must include 'pk' as the primary key of the theme.

            Returns:
                Response: A response object containing the theme data as a JSON object.
        """
        data = list(Theme.objects.filter(id=kwargs["pk"]).values())
        return Response(data)

    def add(self, request, *args, **kwargs):
        """
        Adds a new theme based on provided request data.

            This method validates the incoming request data using the
            ThemeSerializer, saves the data if valid, and returns a response
            indicating the success or failure of the operation.

            Args:
                request: The HTTP request object containing the data to be added.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing a message and status code.
        """
        themes_serializer_data = ThemeSerializer(data=request.data)
        if themes_serializer_data.is_valid():
            themes_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response(
                {"message": "Added Sucessfully", "status": status_code}, status_code
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "please fill the datails", "status": status_code},
                status_code,
            )

    def delete(self, request, *args, **kwargs):
        """
        Delete a theme by its ID.

            This method attempts to delete a theme from the database using the ID
            provided in the keyword arguments. If the theme is successfully deleted,
            it returns a success message along with the HTTP status code. If the
            theme does not exist, it returns an error message with an appropriate
            status code.

            Args:
                request: The request object containing information about the
                         HTTP request.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments that should include 'pk', which is
                          the ID of the theme to be deleted.

            Returns:
                A Response object indicating the result of the delete operation,
                along with an appropriate HTTP status code.
        """
        themes_data = Theme.objects.filter(id=kwargs["pk"])
        if themes_data:
            themes_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response(
                {"message": "Deleted Sucessfully", "status": status_code}, status_code
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "Data not found", "status": status_code}, status_code
            )

    def getBySubjectId(self, request, *args, **kwargs):
        """
        Retrieve themes associated with a specific subject ID.

            This method queries the database for themes that are linked to a
            particular subject ID, provided through the request's keyword arguments.
            It returns a response containing a list of the relevant themes.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments, expected to include 'subject_id'
                    which specifies the ID of the subject for which themes are
                    being fetched.

            Returns:
                Response: A response object containing a list of themes associated
                with the specified subject ID in JSON format.
        """
        data = list(Theme.objects.filter(id_subject=kwargs["subject_id"]).values())
        return Response(data)


class CourseView(viewsets.ModelViewSet):
    """
    A view class for managing courses within the application.

    This class provides methods for adding, retrieving, listing, deleting,
    and filtering courses based on various criteria such as subject ID
    and expert ID. It serves as an interface between the incoming HTTP
    requests and the underlying data model of courses.

    Attributes:
        queryset: A collection of Course objects from the database.
        serializer_class: The serializer to be used for validating and
            formatting course data.
        CourseSerializer: A specific serializer class for Course instances.

    Methods:
        add: Adds a new course based on the provided request data.
        retrieve: Retrieves course data based on the provided primary key.
        list: Retrieves a list of all Course objects.
        delete: Deletes a course identified by the primary key.
        getBySubjectId: Retrieves courses associated with a specific subject ID.
        getByIdExpert: Retrieves courses associated with a specific expert.
        getExpertInfo: Retrieves expert information based on the provided
            expert and subject IDs.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def add(self, request, *args, **kwargs):
        """
        Add a new course based on the provided request data.

            This method processes the incoming request to add a new course
            entry in the system. It checks the validity of the provided data
            and handles the creation of a course either through a serializer
            or by manually instantiating a Course object based on the input.

            Args:
                request: The HTTP request object containing the data to add the course.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing either a success message with a
                status code of 201 if the course is added successfully, or an
                error message with a relevant status code if there are issues
                with the input data.
        """
        data = request.data
        id_expert = data.get("id_expert")
        name_course = data.get("name_course")
        id_subject = data.get("id_subject")
        description = data.get("description")

        course_serializer_data = CourseSerializer(data=data)
        if course_serializer_data.is_valid(raise_exception=True):
            course_serializer_data.save()
            return Response(
                {"message": "Added Sucessfully", "status": status.HTTP_201_CREATED},
                status=status.HTTP_201_CREATED,
            )
        else:
            if not name_course or not id_subject:
                return Response(
                    {
                        "error": "Both name_course and id_subject are required.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            try:
                subject = Subject.objects.get(id=id_subject)
            except Subject.DoesNotExist:
                return Response(
                    {
                        "error": f"Subject with id {id_subject} does not exist.",
                        "status": status.HTTP_400_BAD_REQUEST,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            course = Course(name_course=name_course, id_subject=subject)
            course.save()
            return Response(
                {"message": "Added Sucessfully", "status": status.HTTP_201_CREATED},
                status=status.HTTP_201_CREATED,
            )

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve course data based on the provided primary key.

            This method retrieves a list of course data from the database using
            the primary key provided in the request's keyword arguments. It filters
            the Course objects accordingly and returns the data in a response format.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Additional positional arguments (not used in this method).
                **kwargs: Keyword arguments containing 'pk' as the primary key to filter the Course objects.

            Returns:
                Response: A response object containing the list of course data.
        """
        data = list(Course.objects.filter(id=kwargs["pk"]).values())
        return Response(data)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all Course objects.

            This method fetches all Course instances from the database and returns
            them in a serialized format in the response.

            Args:
                request: The HTTP request object.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                A Response object containing a list of all Course instances in
                serialized format.
        """
        data = list(Course.objects.all().values())
        return Response(data)

    def delete(self, request, *args, **kwargs):
        """
        Delete a course identified by the primary key.

            This method attempts to delete a course from the database based on
            the provided primary key. If the course exists, it will be deleted
            and a success message will be returned. If the course does not
            exist, an error message will be returned.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: A dictionary of keyword arguments, expected to contain
                    the primary key ('pk') of the course to be deleted.

            Returns:
                A Response object containing a message about the outcome of the
                deletion operation and the corresponding HTTP status code.
        """
        course_data = Course.objects.filter(id=kwargs["pk"])
        if course_data:
            course_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response(
                {"message": "Deleted Sucessfully", "status": status_code}, status_code
            )
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(
                {"message": "Data not found", "status": status_code}, status_code
            )

    def getBySubjectId(self, request, *args, **kwargs):
        """
        Retrieves courses associated with a specific subject ID.

            This method queries the database for courses that match the given
            subject ID and returns the result as a response.

            Args:
                request: The request object containing metadata about the request.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments, including 'subject_id' that
                    specifies the ID of the subject to filter courses by.

            Returns:
                A Response object containing a list of courses associated with the
                specified subject ID.
        """
        data = list(Course.objects.filter(id_subject=kwargs["subject_id"]).values())
        return Response(data)

    def getByIdExpert(self, request, *args, **kwargs):
        """
        Retrieve courses associated with a specific expert.

            This method queries the database for all courses that are linked to the
            expert identified by the specified expert ID. It returns the course data
            in a serialized format.

            Args:
                request: The HTTP request object containing the request data.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments containing 'expert_id', which specifies
                    the ID of the expert whose courses are to be retrieved.

            Returns:
                A Response object containing a list of courses associated with the
                expert, formatted as a JSON response.
        """
        data = list(Course.objects.filter(id_expert=kwargs["expert_id"]).values())
        return Response(data)

    def getExpertInfo(self, request, *args, **kwargs):
        """
        Retrieve expert information based on the provided expert and subject IDs.

            This method queries the database for courses associated with a specific expert
            and subject, returning the data in a response format.

            Args:
                request: The HTTP request object that contains contextual information.
                *args: Additional positional arguments.
                **kwargs: A dictionary of keyword arguments that must include:
                    expert_id: The ID of the expert whose information is being requested.
                    subject_id: The ID of the subject related to the expert.

            Returns:
                A Response object containing a list of course data related to the expert
                and subject.
        """
        data = list(
            Course.objects.filter(id_expert=kwargs["expert_id"])
            .filter(id_subject=kwargs["subject_id"])
            .values()
        )
        return Response(data)
