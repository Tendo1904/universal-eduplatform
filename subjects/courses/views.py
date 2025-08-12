from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import *
from .serializers import*

class SubjectView(viewsets.ModelViewSet):
    """
    Class for handling subjects data.
    
        Class Attributes:
        - queryset: Set of subjects.
        - serializer_class: Serializer for subjects.
        - SubjectSerializer: Serizalizer for subjects.
    
        Class Methods:
        - list: Retrieves a list of subjects.
        - retrieve: Retrieves a specific subject.
        - add: Adds a new subject.
        - delete: Deletes a subject.
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all subjects.
        
        Args:
        - self: The instance of the class.
        - request: Request object containing details of the HTTP request.
        
        Returns:
        - list: A list of dictionaries containing details of all subjects retrieved from the database.
        """
        data = list(Subject.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve data from the database based on the provided ID.
                
            Parameters:
            - request: A request object containing information about the HTTP request.
            - *args: Additional positional arguments.
            - **kwargs: Additional keyword arguments where 'pk' is the primary key used for data retrieval.
            
            Returns:
            - Response: An HTTP response containing the retrieved data.
        """
        data = list(Subject.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def add(self, request, *args, **kwargs):
        """
        Adds a subject by creating a new record in the database using the provided request data.
        
        Parameters:
        - self: The instance of the class.
        - request: The request object containing data for the new subject.
        
        Returns:
        A Response object containing a message and status code based on the success of the subject creation.
        
        Args:
        - request: The request object containing data for the new subject.
        
        Return:
        - A Response object containing a message and status code based on the success or failure of the subject creation.
        """
        subject_serializer_data = SubjectSerializer(data=request.data)
        if subject_serializer_data.is_valid():
            subject_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Added Sucessfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill the datails", "status": status_code}, status_code)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a subject object from the database based on the provided ID.
        
        Args:
            request: The request object containing metadata about the incoming request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments containing the subject ID ('pk').
        
        Returns:
            Response: A JSON response indicating the status of the deletion operation.
        """
        subject_data = Subject.objects.filter(id=kwargs['pk'])
        if subject_data:
            subject_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Deleted Sucessfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Data not found", "status": status_code}, status_code)

class ThemeView(viewsets.ModelViewSet):
    """
    This class represents a view for managing themes related to a subject in an application.
    
        Class Attributes:
        - queryset: The query set used by the view to retrieve themes.
        - serializer_class: The serializer class used to serialize themes data.
        - ThemeSerializer: The serializer class specifically for themes.
    
        Class Methods:
        - list: Retrieves a list of themes associated with a subject.
        - retrieve: Retrieves details of a specific theme.
        - add: Adds a new theme to the subject.
        - delete: Deletes a theme from the subject.
        - getBySubjectId: Retrieves themes based on the subject ID.
    """

    queryset =Theme.objects.all()
    serializer_class = ThemeSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all themes.
                
            Parameters:
            - request: The HTTP request object.
            
            Returns:
            - Response: A Response object containing the list of all themes.
        """
        data = list(Theme.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve data for a specific theme based on the provided ID.
        
        Args:
        - request: the request object containing data for processing.
        - *args: additional positional arguments.
        - **kwargs: additional keyword arguments, expected 'pk' for the theme ID.
        
        Returns:
        - Response: a response containing the data for the theme with the specified ID.
        """
        data = list(Theme.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def add(self, request, *args, **kwargs):
        """
        Adds a theme based on the provided request data.
            
            Parameters:
            - self: the class instance
            - request: the request object containing data for the new theme
            
            Returns:
            - Response: Returns a Response object with a message and status code based on the success of adding a theme.
        """
        themes_serializer_data = ThemeSerializer(data=request.data)
        if themes_serializer_data.is_valid():
            themes_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Added Sucessfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "please fill the datails", "status": status_code}, status_code)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a theme object based on the provided ID.
        
        Args:
        - self: The object instance.
        - request: The request object containing information.
        
        Returns:
        - dict: A dictionary containing a message and status code indicating the success or failure of the deletion process.
        """
        themes_data = Theme.objects.filter(id=kwargs['pk'])
        if themes_data:
            themes_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Deleted Sucessfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Data not found", "status": status_code}, status_code)
    def getBySubjectId(self, request, *args, **kwargs):
        """
        Retrieves themes related to the specified subject ID.
        
        Args:
        - self: The instance of the ThemeView class.
        - request: The request object containing information needed for theme retrieval.
        - *args: Additional positional arguments.
        - **kwargs: Additional keyword arguments, including 'subject_id'.
        
        Returns:
        Response: A response containing a list of themes data related to the specified subject ID.
        """
        data = list(Theme.objects.filter(id_subject=kwargs['subject_id']).values())
        return Response(data)

class CourseView(viewsets.ModelViewSet):
    """
    This class represents a view for managing courses. It provides functionality for adding, retrieving, listing, and deleting courses. Additionally, it includes methods for getting courses by subject ID, expert ID, and expert information.
    
        Class Attributes:
        - queryset
        - serializer_class
        - CourseSerializer
    
        Class Methods:
        - add: Method to add a course
        - retrieve: Method to retrieve a course
        - list: Method to list all courses
        - delete: Method to delete a course
        - getBySubjectId: Method to get courses by subject ID
        - getByIdExpert: Method to get courses by expert ID
        - getExpertInfo: Method to get expert information
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def add(self, request, *args, **kwargs):
        """
        Adds a new course to the system based on the provided request data.
        
        Args:
        - self: The instance of the class.
        - request: The request object containing data for the new course.
        
        Returns:
        A Response object indicating the success or failure of the addition.
        """
        data = request.data
        id_expert = data.get('id_expert')
        name_course = data.get('name_course')
        id_subject = data.get('id_subject')
        description = data.get('description')

        course_serializer_data = CourseSerializer(data=data)
        if course_serializer_data.is_valid(raise_exception=True):
            course_serializer_data.save()
            return Response({"message": "Added Sucessfully", "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        else:
            if not name_course or not id_subject:
                return Response({"error": "Both name_course and id_subject are required.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            try:
                subject = Subject.objects.get(id=id_subject)
            except Subject.DoesNotExist:
                return Response({"error": f"Subject with id {id_subject} does not exist.",  "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            course = Course(name_course=name_course, id_subject=subject)
            course.save()
            return Response({"message": "Added Sucessfully",  "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
        
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the data for a specific course based on the provided ID.
        
        Args:
        - self: The instance of the class.
        - request: The HTTP request object containing information.
        - *args: Variable length argument list.
        - **kwargs: Arbitrary keyword arguments.
        
        Returns:
        Response: A JSON response containing the data of the course with the specified ID.
        """
        data = list(Course.objects.filter(id=kwargs['pk']).values())
        return Response(data)    
    
    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of all courses from the database and returns them as a response.
        
        Args:
            self: The instance of the class.
            request: The HTTP request object.
        
        Returns:
            Response: A JSON response containing the list of all courses.
        """
        data = list(Course.objects.all().values())
        return Response(data)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a course from the database based on the provided course ID.
        
        Parameters:
        - request: The request object containing metadata about the HTTP request.
        - kwargs['pk']: The primary key of the course to be deleted.
        
        Returns:
        - dict: A dictionary containing the success or failure message along with the status code.
        """
        course_data = Course.objects.filter(id=kwargs['pk'])
        if course_data:
            course_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Deleted Sucessfully", "status": status_code}, status_code)
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Data not found", "status": status_code}, status_code)
    def getBySubjectId(self, request, *args, **kwargs):
        """
        Fetches course data based on a provided subject ID.
        
        Args:
            self: The instance of the class.
            request: The request object containing information required to retrieve course data.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments, subject_id is expected in kwargs.
        
        Returns:
            Response: A response containing the course data associated with the specified subject ID.
        """
        data = list(Course.objects.filter(id_subject=kwargs['subject_id']).values())
        return Response(data)
    def getByIdExpert(self, request, *args, **kwargs):
        """
        Summary:
            Retrieves a list of courses associated with a specific expert ID.
        
        Args:
            - request: The HTTP request object.
        
        Returns:
            A Response object containing a list of courses related to the specified expert ID.
        """
        data = list(Course.objects.filter(id_expert=kwargs['expert_id']).values())
        return Response(data)
    def getExpertInfo(self, request, *args, **kwargs):
        """
        Get information about an expert based on their ID and subject ID.
                
                Parameters:
                - self: The object instance.
                - request: The request object containing information for the expert retrieval.
                - kwargs['expert_id']: The ID of the expert.
                - kwargs['subject_id']: The ID of the subject.
                
                Returns:
                - Response: A response containing the expert information retrieved from the database.
        """
        data = list(Course.objects.filter(id_expert=kwargs['expert_id']).filter(id_subject=kwargs['subject_id']).values())
        return Response(data)
