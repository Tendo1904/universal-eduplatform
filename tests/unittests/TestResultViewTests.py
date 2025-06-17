from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from tests.models import Test, Question, Answer, Result, Solutions
from django.urls import reverse


class ResultsViewTests(TestCase):
    """
    Tests for the Results API endpoints.

        This class contains test cases for testing the Results API, including the addition,
        retrieval, and listing of test results for users. It sets up the necessary test
        environment and provides a series of assertions to verify the correctness of the
        API responses.

        Methods:
            - setUp
            - test_add_result
            - test_list_results
            - test_get_by_result_id
            - test_get_by_student_test_id
            - test_get_by_student_id
            - test_get_by_test_id
            - test_full_student_test_id
            - test_full_student_id
            - test_full_test_id

        Attributes:
            client
            test
            question
            answer
            result
            solution

        The methods in this class interact with various API endpoints to ensure that
        the Results API behaves as expected. The attributes are used to set up the
        testing environment with necessary instances of models related to the results
        being tested.

    """

    def setUp(self):
        """
        Sets up the test environment for the class.

            This method is called before each test case is run. It initializes the
            API client and creates test instances for Test, Question, Answer,
            Result, and Solutions models.

            Attributes:
                client: An instance of the APIClient to make requests.
                test: A test instance created with preset attributes.
                question: A question instance associated with the created test.
                answer: An answer instance associated with the created question.
                result: A result instance associated with a user and the created test.
                solution: A solution instance that links the result to the question and answer.

            Returns:
                None
        """
        self.client = APIClient()
        self.test = Test.objects.create(
            author_id=1, subject_id=1, theme_id=1, expert_id=1, max_points=100
        )
        self.question = Question.objects.create(
            id_test=self.test, question_text="Sample Question"
        )
        self.answer = Answer.objects.create(
            id_question=self.question, answer_text="Sample Answer", is_correct=True
        )
        self.result = Result.objects.create(
            id_user=1, id_test=self.test.id, points_user=0
        )
        self.solution = Solutions.objects.create(
            id_result=self.result, id_question=self.question, id_answer=self.answer
        )

    def test_add_result(self):
        """
        Tests the addition of a test result for a user.

            This method prepares a data dictionary containing user and test information,
            then sends a POST request to the 'results-add' endpoint to add the test result
            for the user. It asserts that the response status code indicates successful
            creation of the result.

            Parameters:
                None

            Returns:
                None
        """
        data = {
            "id_user": 1,
            "id_test": self.test.id,
            "subject": "Math",
            "theme": "Algebra",
            "solutions": [
                {"id_question": self.question.id, "id_answer": self.answer.id}
            ],
        }
        response = self.client.post(reverse("results-add"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_results(self):
        """
        Tests the results list endpoint for a successful response.

            This method sends a GET request to the results list endpoint and
            asserts that the response status code is 200 OK, indicating that
            the request was successful.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(reverse("results-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_result_id(self):
        """
        Tests the endpoint for retrieving a result by its ID.

            This method sends a GET request to the 'results-get-by-id' endpoint
            using the ID of a result and asserts that the response status code
            is 200 OK.

            Args:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("results-get-by-id", kwargs={"id": self.result.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_student_test_id(self):
        """
        Tests the retrieval of results by student test ID.

            This method sends a GET request to the results endpoint with a specific test ID and student ID,
            and asserts that the response status code is 200 (OK).

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse(
                "results-get-by-student-test-id",
                kwargs={"testId": self.test.id, "studentId": 1},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_student_id(self):
        """
        Tests the retrieval of results by a given student ID.

            This method sends a GET request to the endpoint that retrieves results
            associated with a specific student ID and asserts that the response status
            code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("results-get-by-student-id", kwargs={"studentId": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_by_test_id(self):
        """
        Tests the retrieval of results by test ID.

            This method sends a GET request to an endpoint to fetch results associated
            with a specific test ID and asserts that the response status code is
            200 OK, indicating a successful retrieval.

            Args:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("results-get-by-test-id", kwargs={"testId": self.test.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_student_test_id(self):
        """
        Test the response of the full student test ID endpoint.

            This method sends a GET request to the 'results-full-student-test-id' endpoint with
            specific test and student IDs, and asserts that the response status code is 200 OK.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse(
                "results-full-student-test-id",
                kwargs={"testId": self.test.id, "studentId": 1},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_student_id(self):
        """
        Tests the response of the full student ID results endpoint.

            This method sends a GET request to the 'results-full-student-id' endpoint with a specific
            student ID and asserts that the response status code is 200 OK.

            Returns:
                None
        """
        response = self.client.get(
            reverse("results-full-student-id", kwargs={"studentId": 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_full_test_id(self):
        """
        Tests the endpoint for retrieving a full test by its ID.

            This method sends a GET request to the 'results-full-test-id' endpoint
            with the associated test ID and asserts that the response status code
            is 200 OK, indicating a successful retrieval of the test data.

            Parameters:
                None

            Returns:
                None
        """
        response = self.client.get(
            reverse("results-full-test-id", kwargs={"testId": self.test.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    ResultsViewTests()
