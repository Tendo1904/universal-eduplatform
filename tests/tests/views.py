from rest_framework import status, generics, viewsets
from .models import Test, Question, Answer,Solutions, Result
from .serializers import (TestSerializer,
                          QuestionSerializer,
                          AnswerSerializer,
                          TestListSerializer,
                          TestGetSerializer,
                          CorrectAnswerSerializer,
                          ResultsSerializer,
                          SolutionsResultsSerializer,
                          TestUserSerializer,
                          AnswerAllSerializer,
                          SolutionsSerializer)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .calculations import formula_1

class ResultsView(viewsets.ModelViewSet):
    """
    A class to represent a view for displaying and interacting with results data.
    
        Class Attributes:
        - queryset: Represents the data queried for results.
        - serializer_class: Defines the serializer class used for serializing/deserializing data.
    
        Class Methods:
        - list: Retrieves and returns a list of all results data.
        - create: Creates a new result entry.
        - retrieve: Retrieves and returns a specific result entry.
        - update: Updates an existing result entry.
        - destroy: Deletes a result entry.
    """

    serializer_class = ResultsSerializer

    @swagger_auto_schema(tags=["Result"], operation_description="add student's result")
    def add(self, request, *args, **kwargs):
        """
        Adds a student's result to the system.
        
        Parameters:
        - self: The instance of the class.
        - request: The request object containing data about the student's result.
        
        Returns:
        - Response: A success message along with the status code of the operation.
        
        Args:
        - id_user: The ID of the user associated with the result.
        - id_test: The ID of the test for which the result is being added.
        - subject: The subject of the test result.
        - theme: The theme of the test result.
        - solutions: A list of solutions provided by the student for the test.
        
        Return:
        - Response: A success message along with the status code of the operation after adding the student's result.
        """
        data = request.data
        id_user = data.get('id_user')
        id_test = data.get('id_test')
        subject = data.get('subject')
        theme = data.get('theme')
        results = data.get('solutions', [])

        serializer = TestUserSerializer(data={'id_user': id_user, 'id_test': id_test, 'subject': subject, 'theme': theme})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id_result = list(Result.objects.filter(id_user=id_user).filter(id_test=id_test).values_list('id', flat=True))[-1]

        result_data = []
        for result in results:
            result['id_result'] = id_result
            serializer = SolutionsResultsSerializer(data=result)
            if serializer.is_valid():
                serializer.save()
                result_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        result = Result.objects.get(pk=id_result)
        result.points_user = formula_1(id_result)
        result.save()
        test = Test.objects.get(id=id_test)
        times_solved = test.times_solved + 1
        test.times_solved = times_solved
        test.save()
        return Response({"message": "Added Sucessfully",  "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
            
    @swagger_auto_schema(tags=["Result"], operation_description="get all results in database")
    def list(self, request, *args, **kwargs):
        """
        Retrieves all results from the database and serializes them using ResultsSerializer.
        
        Args:
        - request: The HTTP request object.
        
        Returns:
        - Response: An HTTP response object containing serialized data of all results with status code 200.
        """
        results = Result.objects.all()
        serializer = ResultsSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve a result by id")
    def getByResultId(self, request, *args, **kwargs):
        """
        Retrieve a result by id.
        
        Args:
        - request: HttpRequest object containing metadata about the request.
        - id: The unique identifier of the result to retrieve.
        
        Returns:
        - Response: Serialized data of the retrieved result with a status code of HTTP 200 OK.
        - Note: This method is responsible for retrieving a specific result identified by the provided id.
        """
        data = get_object_or_404(Result, pk=kwargs['id'])
        serializer = ResultsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Result"],  operation_description="retrieve all student's results (IDs) for a test")
    def getByStudentTestId(self, request, *args, **kwargs):
        """
        Retrieve all student's results (IDs) for a specific test.
        
        Args:
            - self: the instance of the class
            - request: the HTTP request object
            - args: Variable positional arguments
            - kwargs: Variable keyword arguments containing 'testId' and 'studentId'
        
        Returns:
            - Response: a list of result IDs for the specified test and student
        """
        data = list(Result.objects.filter(id_test=kwargs['testId']).filter(id_user=kwargs['studentId']).values_list('id', flat = True))
        return Response(data)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve all student's results (IDs)")
    def getByStudentId(self, request, *args, **kwargs):
        """
        Retrieve all student's results by their student ID.
        
        Args:
            - self: The object instance.
            - request: The request object containing metadata about the HTTP request.
            - args: Additional arguments.
            - kwargs: Additional keyword arguments.
        
        Returns:
            - List: A list of result IDs associated with the student ID provided.
        """
        data = list(Result.objects.filter(id_user=kwargs['studentId']).values_list('id', flat=True))
        return Response(data)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve all results (IDs) for a test")
    def getByTestId(self, request, *args, **kwargs):
        """
        Fetches all result IDs for a specific test based on the provided test ID.
        
        Args:
            self: The object instance.
            request: The HTTP request object containing metadata.
            *args: Additional arguments.
            **kwargs: Additional keyword arguments, including 'testId'.
        
        Returns:
            list: A list of result IDs corresponding to the specified test.
        """
        data = list(Result.objects.filter(id_test=kwargs['testId']).values_list('id', flat=True))
        return Response(data)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve all student's solutions for a test")
    def fullStudentTestId(self, request, *args, **kwargs):
        """
        Retrieve all student's solutions for a test.
            
            Parameters:
            - request: The HTTP request object.
            - *args: Additional positional arguments.
            - **kwargs: Additional keyword arguments, including 'testId' and 'studentId'.
            
            Returns:
            - Response: A response containing the serialized data of the student's solutions for the test.
            - status: The HTTP status of the response (HTTP_200_OK in this case).
        """
        data = Result.objects.filter(id_test=kwargs['testId']).filter(id_user=kwargs['studentId'])
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve all student's solutions for all tests")
    def fullStudentId(self, request, *args, **kwargs):
        """
        Retrieve all solutions for all tests submitted by a specific student.
        
        Args:
            self: Instance of the class.
            request: Object representing the HTTP request.
            *args: Variable-length argument list passed to the method.
            **kwargs: Arbitrary keyword arguments passed to the method. It contains the student's ID.
        
        Returns:
            Response: Serialized data containing all solutions for the specified student's tests.
        """
        data = Result.objects.filter(id_user=kwargs['studentId'])
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=["Result"], operation_description="retrieve all solutions for a test")
    def fullTestId(self, request, *args, **kwargs):
        """
        Summary:
                    Retrieves and returns all solutions associated with the specified test.
                
                Description:
                    Parameters:
                        self: The instance of the class.
                        request: The request object containing information.
                        *args: Additional positional arguments.
                        **kwargs: Additional keyword arguments.
                    
                    Return:
                        Response: Serialized data for all solutions associated with the specified test.
        """
        data = Result.objects.filter(id_test=kwargs['testId'])
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAPIView(viewsets.ModelViewSet):
    """
    This class represents a REST API view for testing purposes.
    
        Attributes:
        - serializer_class: The serializer class to use for serializing and deserializing data.
        - TestSerializer: An instance of the TestSerializer class for handling serialization tasks.
    
        Class Methods:
        - add: Adds data to the API.
        - update: Updates existing data in the API.
        - delete: Deletes data from the API.
    """

    serializer_class = TestSerializer

    @swagger_auto_schema(tags=["Test"], operation_description="creates a test")

    def add(self, request, *args, **kwargs):
        """
        Add a new test with questions and answers to the database.
                
                Parameters:
                    - request: The request object containing data for creating the test.
                  
                Returns:
                    - Response: A response indicating the success of the operation.
                    - status: The status of the HTTP response.
        """
        data = request.data
        serializer = TestSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create Test instance
        test_instance = Test.objects.create(
            author_id=data['author_id'],
            subject_id=data['subject_id'],
            theme_id=data['theme_id'],
            expert_id=data['theme_id'],
            max_points=data['max_points']
        )

        # Create Question and Answer instances
        for question_data in data['questions']:
            answers_data = question_data.pop('answers', [])

            question_instance = Question.objects.create(id_test=test_instance, **question_data)

            for answer_data in answers_data:
                Answer.objects.create(id_question=question_instance, **answer_data)

        return Response({"message": "Added Sucessfully",  "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    
class TestListView(viewsets.ModelViewSet):
    """
    This class represents a view for displaying a list of tests.
    
        Class Attributes:
        - serializer_class: The serializer class used for serializing test objects.
        - TestListSerializer: The specific serializer for test objects.
        - queryset: The queryset used to retrieve test objects from the database.
    
        Class Methods:
        - get: Retrieves and returns a list of tests.
    """

    serializer_class = TestListSerializer
    queryset = Test.objects.all()

    @swagger_auto_schema(tags=["Test"], operation_description="retrieve a list of tests based on subject and theme IDs")
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of tests based on given subject and theme IDs.
        
        Args:
        - request: The request object for fetching data.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments containing 'subject_id' and 'theme_id'.
        
        Returns:
        - Response: A response containing the serialized data of the retrieved tests.
        """
        data = Test.objects.filter(subject_id=kwargs['subject_id']).filter(theme_id=kwargs['theme_id']).values()
        print(data)
        serializer = TestListSerializer(data, many=True)
        return Response(serializer.data)
        
class TestGetView(viewsets.ModelViewSet):
    """
    This class represents a view that retrieves data from the database.
    
        Class Methods:
        - get: Retrieves data based on the provided parameters.
    
        Class Attributes:
        - serializer_class: Specifies the serializer class to be used for data serialization.
        - TestGetSerializer: An instance of the TestGetSerializer class.
        - queryset: Represents the database query for retrieving data.
    """

    serializer_class = TestGetSerializer
    queryset = Test.objects.all()

    @swagger_auto_schema(tags=["Test"], operation_description="retrieve a test without correct answers")
    def get(self, request, *args, **kwargs):
        """
        Retrieves a test without correct answers.
        
        Args:
            self: The object instance.
            request: The request object.
        
        Returns:
            Response: A JSON response containing the serialized test data.
            TestGetSerializer: A serializer instance for the retrieved test.
        """
        test =  get_object_or_404(Test, pk=kwargs['pk'])
        serializer = TestGetSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class GetAllCorrectAnswersView(viewsets.ModelViewSet):
    """
    Class for retrieving all correct answers.
    
        Class Methods:
        - get: Retrieve all correct answers.
    
        Class Attributes:
        - serializer_class: The serializer class used for serializing correct answers.
        - CorrectAnswerSerializer: Serializer for correct answers.
        - queryset: The queryset for retrieving correct answers.
    """

    serializer_class = CorrectAnswerSerializer
    queryset = Question.objects.all()

    @swagger_auto_schema(tags=["Test"], operation_description="get correct answers for every question in a test")

    def get(self, request, *args, **kwargs):
        """
        Get correct answers for every question in a specific test.
        
        Args:
        - self: Instance of the class.
        - request: HTTP request object.
        
        Return:
        - List of dictionaries containing data on correct answers for each question in the test.
        """
        questions = Question.objects.filter(id_test=kwargs['pk'])

        correct_answers_data = []

        for question in questions:
            answers = Answer.objects.filter(id_question=question.pk).filter(is_correct=True).values()
            data_answers = [answer['answer_text'] for answer in answers]
            correct_answers_data.append({
                    'id_question': question.pk,
                    'correct_answers': data_answers,
                })

        return Response(correct_answers_data, status=status.HTTP_200_OK)

class GetAllCorrectAnswersByQuestionView(viewsets.ModelViewSet):
    """
    A view class for retrieving all correct answers for a specific question.
    
        Class Methods:
        - get: Retrieves all correct answers for a specific question.
    """

    serializer_class = AnswerAllSerializer

    @swagger_auto_schema(tags=["Test"], operation_description="get correct answers for a one question")

    def get(self, request, *args, **kwargs):
        """
        Get correct answers for a specific question. 
        
        Args:
            request: The HTTP request object.
            kwargs: A dictionary containing the question primary key under the key 'question_pk'.
            
        Returns:
            Response: JSON response containing the correct answers for the specified question.
        """
        answers = Answer.objects.filter(id_question=kwargs['question_pk']).filter(is_correct=True).values()
        serializer = AnswerAllSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
