from rest_framework import status, generics, viewsets
from .models import Test, Question, Answer, Solutions, Result
from .serializers import (
    TestSerializer,
    QuestionSerializer,
    AnswerSerializer,
    TestListSerializer,
    TestGetSerializer,
    CorrectAnswerSerializer,
    ResultsSerializer,
    SolutionsResultsSerializer,
    TestUserSerializer,
    AnswerAllSerializer,
    SolutionsSerializer,
)
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .calculations import formula_1


class ResultsView(viewsets.ModelViewSet):
    """
    A class to handle HTTP requests related to student test results.

    This class provides methods for adding student results, retrieving results
    by various criteria, and fetching detailed solutions based on student and test IDs.

    Attributes:
        serializer_class: The class used for serializing result data.
        ResultsSerializer: The serializer specifically designed for handling results.

    Methods:
        add: Add a student's result to the system.
        list: Retrieve all results from the database.
        getByResultId: Retrieve a result by its identifier.
        getByStudentTestId: Retrieve all student's results (IDs) for a specific test.
        getByStudentId: Retrieve all results for a given student.
        getByTestId: Retrieve all result IDs associated with a specific test.
        fullStudentTestId: Retrieves all solutions for a specific student's test.
        fullStudentId: Retrieve all solutions for a specific student.
        fullTestId: Retrieve all solutions for a specified test.
    """

    serializer_class = ResultsSerializer

    @swagger_auto_schema(tags=["Result"], operation_description="add student's result")
    def add(self, request, *args, **kwargs):
        """
        Add a student's result to the system.

            This method processes a request to add a student's results for a specific test,
            including validation and saving the results. If the student and test details are valid,
            it updates the test statistics accordingly.

            Args:
                request: The HTTP request containing the data for the operation, including user ID,
                         test ID, subject, theme, and solutions.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object indicating the outcome of the operation.
                On success, it returns a message along with a status code of 201 (Created).
                If there are validation errors, it returns a Response with the errors and a
                status code of 400 (Bad Request).
        """
        data = request.data
        id_user = data.get("id_user")
        id_test = data.get("id_test")
        subject = data.get("subject")
        theme = data.get("theme")
        results = data.get("solutions", [])

        serializer = TestUserSerializer(
            data={
                "id_user": id_user,
                "id_test": id_test,
                "subject": subject,
                "theme": theme,
            }
        )
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        id_result = list(
            Result.objects.filter(id_user=id_user)
            .filter(id_test=id_test)
            .values_list("id", flat=True)
        )[-1]

        result_data = []
        for result in results:
            result["id_result"] = id_result
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
        return Response(
            {"message": "Added Sucessfully", "status": status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
        )

    @swagger_auto_schema(
        tags=["Result"], operation_description="get all results in database"
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve all results from the database.

            This method fetches all records from the Result model and returns them
            in a serialized format as a response. It is intended for use with
            the Swagger API documentation.

            Args:
                request: The HTTP request object containing data about the request.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments.

            Returns:
                A Response object containing the serialized data of all results
                and an HTTP status code indicating the success of the operation.
        """
        results = Result.objects.all()
        serializer = ResultsSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Result"], operation_description="retrieve a result by id"
    )
    def getByResultId(self, request, *args, **kwargs):
        """
        Retrieve a result by its identifier.

            This method retrieves a Result object based on the provided identifier in the URL
            and returns its serialized data in the response.

            Args:
                request: The HTTP request object containing the incoming request data.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments containing the identifier of the Result object
                          to be retrieved.

            Returns:
                Response: A Response object containing the serialized data of the retrieved
                          Result and a status code of 200 OK.
        """
        data = get_object_or_404(Result, pk=kwargs["id"])
        serializer = ResultsSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Result"],
        operation_description="retrieve all student's results (IDs) for a test",
    )
    def getByStudentTestId(self, request, *args, **kwargs):
        """
        Retrieve all student's results (IDs) for a specific test.

            This method queries the database to get all result IDs associated
            with a given test ID and student ID. It returns the result IDs
            in a list format.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments including:
                    - testId: The ID of the test for which results are being retrieved.
                    - studentId: The ID of the student whose results are being queried.

            Returns:
                A Response object containing a list of result IDs for the specified
                student and test.
        """
        data = list(
            Result.objects.filter(id_test=kwargs["testId"])
            .filter(id_user=kwargs["studentId"])
            .values_list("id", flat=True)
        )
        return Response(data)

    @swagger_auto_schema(
        tags=["Result"], operation_description="retrieve all student's results (IDs)"
    )
    def getByStudentId(self, request, *args, **kwargs):
        """
        Retrieve all results for a given student.

            This method queries the database for all result IDs associated with
            the specified student ID and returns them in a response.

            Args:
                request: The HTTP request object.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments. Must include 'studentId'
                          which specifies the ID of the student whose results are to be retrieved.

            Returns:
                Response: A response containing a list of result IDs associated
                          with the specified student.
        """
        data = list(
            Result.objects.filter(id_user=kwargs["studentId"]).values_list(
                "id", flat=True
            )
        )
        return Response(data)

    @swagger_auto_schema(
        tags=["Result"], operation_description="retrieve all results (IDs) for a test"
    )
    def getByTestId(self, request, *args, **kwargs):
        """
        Retrieve all result IDs associated with a specific test.

            This method fetches the IDs of all results related to a given test, identified by its test ID.
            It queries the database for results and returns a list of IDs in the response.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments, must include 'testId' to specify which test's results to retrieve.

            Returns:
                Response: A response object containing a list of result IDs associated with the specified test.
        """
        data = list(
            Result.objects.filter(id_test=kwargs["testId"]).values_list("id", flat=True)
        )
        return Response(data)

    @swagger_auto_schema(
        tags=["Result"],
        operation_description="retrieve all student's solutions for a test",
    )
    def fullStudentTestId(self, request, *args, **kwargs):
        """
        Retrieves all solutions for a specific student's test.

            This method filters the results based on the provided test ID and student ID, serializes
            the data, and returns it in the response.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments containing 'testId' and 'studentId'.

            Returns:
                A Response object containing the serialized data and an HTTP status code.
        """
        data = Result.objects.filter(id_test=kwargs["testId"]).filter(
            id_user=kwargs["studentId"]
        )
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Result"],
        operation_description="retrieve all student's solutions for all tests",
    )
    def fullStudentId(self, request, *args, **kwargs):
        """
        Retrieve all solutions for a specific student.

            This method fetches all test solutions associated with a particular student identified by their ID.
            It filters the results based on the student's unique identifier and serializes the data before returning it.

            Args:
                request: The request object containing metadata about the request made to the server.
                *args: Additional positional arguments that may be passed to the method.
                **kwargs: Any keyword arguments passed to the method, including 'studentId' which is used to identify the student.

            Returns:
                A Response object containing the serialized data of the student's solutions and an HTTP status code indicating the result of the operation.
        """
        data = Result.objects.filter(id_user=kwargs["studentId"])
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["Result"], operation_description="retrieve all solutions for a test"
    )
    def fullTestId(self, request, *args, **kwargs):
        """
        Retrieve all solutions for a specified test.

            This method fetches all results associated with a given test ID and
            serializes the data for response.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Additional positional arguments.
                **kwargs: A dictionary of keyword arguments, expected to include
                          'testId' which specifies the ID of the test for which
                          results are to be retrieved.

            Returns:
                A Response object containing serialized test results and an HTTP status code.
        """
        data = Result.objects.filter(id_test=kwargs["testId"])
        serializer = ResultsSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestAPIView(viewsets.ModelViewSet):
    """
    A view for managing tests and their associated questions and answers.

    This class provides an API endpoint to create new tests along with their related questions and answers.

    Attributes:
        serializer_class: The serializer class used for validating and serializing test data.
        TestSerializer: A specific serializer class tailored for handling test data.

    Methods:
        add: Creates a test and its associated questions and answers.

    The `add` method processes a request to create a new test instance and validates the provided data.
    It facilitates the creation of necessary database entries while returning an appropriate response.
    """

    serializer_class = TestSerializer

    @swagger_auto_schema(tags=["Test"], operation_description="creates a test")
    def add(self, request, *args, **kwargs):
        """
        Creates a test and its associated questions and answers.

            This method processes a request to create a new test instance along with its questions and answers.
            It validates the provided data and creates the necessary database entries.

            Args:
                request: The HTTP request object containing the data for the test, questions, and answers.
                *args: Additional positional arguments that can be passed to the method.
                **kwargs: Additional keyword arguments that can be passed to the method.

            Returns:
                A Response object containing a success message and the status code indicating the result of the operation.
        """
        data = request.data
        serializer = TestSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Create Test instance
        test_instance = Test.objects.create(
            author_id=data["author_id"],
            subject_id=data["subject_id"],
            theme_id=data["theme_id"],
            expert_id=data["theme_id"],
            max_points=data["max_points"],
        )

        # Create Question and Answer instances
        for question_data in data["questions"]:
            answers_data = question_data.pop("answers", [])

            question_instance = Question.objects.create(
                id_test=test_instance, **question_data
            )

            for answer_data in answers_data:
                Answer.objects.create(id_question=question_instance, **answer_data)

        return Response(
            {"message": "Added Sucessfully", "status": status.HTTP_201_CREATED},
            status=status.HTTP_201_CREATED,
        )


class TestListView(viewsets.ModelViewSet):
    """
    Handles the retrieval of test records based on specified subject and theme IDs.

    This class is responsible for managing the process of fetching tests from
    the database and returning them in a serialized format suitable for
    client consumption.

    Attributes:
        serializer_class: The serializer used to convert test data into
                          a suitable format for the response.
        TestListSerializer: A specific serializer for formatting test list
                            data.
        queryset: The set of test records fetched from the database.

    Methods:
        get: Retrieve a list of tests based on subject and theme IDs.
    """

    serializer_class = TestListSerializer
    queryset = Test.objects.all()

    @swagger_auto_schema(
        tags=["Test"],
        operation_description="retrieve a list of tests based on subject and theme IDs",
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a list of tests based on subject and theme IDs.

            This method fetches test records from the database that match the specified
            subject and theme IDs. It serializes the data and returns it in the response.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Additional positional arguments that may be passed to the method.
                **kwargs: A dictionary of keyword arguments, which must include:
                    - subject_id: The ID of the subject to filter tests by.
                    - theme_id: The ID of the theme to filter tests by.

            Returns:
                A Response object containing a list of tests serialized into a format
                suitable for client consumption.
        """
        data = (
            Test.objects.filter(subject_id=kwargs["subject_id"])
            .filter(theme_id=kwargs["theme_id"])
            .values()
        )
        print(data)
        serializer = TestListSerializer(data, many=True)
        return Response(serializer.data)


class TestGetView(viewsets.ModelViewSet):
    """
    A view class for retrieving test objects without displaying correct answers.

    This class handles HTTP GET requests to fetch a specific test identified by its primary key,
    serializing the test data for the response while omitting correct answers.

    Attributes:
        serializer_class: The serializer used for formatting the test data.
        TestGetSerializer: A specific serializer class for handling test retrieval.
        queryset: The base queryset used to access test objects in the database.

    Methods:
        get: Retrieves a test without correct answers.

    The `get` method fetches a test object from the database using its primary key. If the test
    is found, it serializes the data and returns it in the response. Otherwise, a 404 error
    is raised.
    """

    serializer_class = TestGetSerializer
    queryset = Test.objects.all()

    @swagger_auto_schema(
        tags=["Test"], operation_description="retrieve a test without correct answers"
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve a test without correct answers.

            This method fetches a test object identified by its primary key from the
            database. If the test is found, it serializes the test data and returns it
            in the response. If the test is not found, a 404 error is raised.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: This must include 'pk' as the key for the primary key of the test to retrieve.

            Returns:
                A Response object containing the serialized test data along with an HTTP status code.
        """
        test = get_object_or_404(Test, pk=kwargs["pk"])
        serializer = TestGetSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllCorrectAnswersView(viewsets.ModelViewSet):
    """
    A view that retrieves all correct answers for questions in a specified test.

    This class handles the logic for fetching the correct answers of questions
    associated with a given test. It is primarily used to provide a structured
    response containing these answers.

    Attributes:
        serializer_class: The serializer used to format the correct answers data.
        CorrectAnswerSerializer: The specific serializer class that defines how
                                 correct answers are serialized.
        queryset: The set of questions being queried for correct answers.

    Methods:
        get: Fetches correct answers for every question in a specified test.

    The `get` method retrieves the questions based on a test ID and collects
    the correct answers for each question, returning them in a standardized
    response format with an HTTP 200 OK status.
    """

    serializer_class = CorrectAnswerSerializer
    queryset = Question.objects.all()

    @swagger_auto_schema(
        tags=["Test"],
        operation_description="get correct answers for every question in a test",
    )
    def get(self, request, *args, **kwargs):
        """
        Fetches correct answers for every question in a specified test.

            This method retrieves the questions associated with a given test ID
            and collects the correct answers for each question. It then returns this
            data in a structured format.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments, including:
                    - pk: The primary key of the test for which to fetch questions.

            Returns:
                A Response object containing the correct answers data for the questions,
                with a status of HTTP 200 OK.
        """
        questions = Question.objects.filter(id_test=kwargs["pk"])

        correct_answers_data = []

        for question in questions:
            answers = (
                Answer.objects.filter(id_question=question.pk)
                .filter(is_correct=True)
                .values()
            )
            data_answers = [answer["answer_text"] for answer in answers]
            correct_answers_data.append(
                {
                    "id_question": question.pk,
                    "correct_answers": data_answers,
                }
            )

        return Response(correct_answers_data, status=status.HTTP_200_OK)


class GetAllCorrectAnswersByQuestionView(viewsets.ModelViewSet):
    """
    A view that retrieves all correct answers associated with a specific question.

    This class handles HTTP GET requests to fetch correct answers for a question
    identified by its primary key. It queries the database for answers marked as
    correct and serializes the results for response.

    Attributes:
        serializer_class: The serializer used for formatting the response data.
        AnswerAllSerializer: The specific serializer class used for answer objects.

    Methods:
        get: Handles the retrieval of correct answers for a specified question.
    """

    serializer_class = AnswerAllSerializer

    @swagger_auto_schema(
        tags=["Test"], operation_description="get correct answers for a one question"
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve correct answers for a specific question.

            This method handles a GET request to fetch all the correct answers associated
            with a given question, identified by its primary key. It queries the database for
            answers marked as correct, serializes the data, and returns it in a response.

            Args:
                request: The HTTP request object containing metadata about the request.
                *args: Additional positional arguments.
                **kwargs: Additional keyword arguments, expected to include 'question_pk'
                          which is the primary key for the question being queried.

            Returns:
                A Response object containing a list of correct answers for the specified question,
                accompanied by an HTTP status code indicating the outcome of the request.
        """
        answers = (
            Answer.objects.filter(id_question=kwargs["question_pk"])
            .filter(is_correct=True)
            .values()
        )
        serializer = AnswerAllSerializer(answers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
