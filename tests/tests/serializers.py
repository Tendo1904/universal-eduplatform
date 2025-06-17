from rest_framework import serializers
from .models import Test, Question, Solutions, Answer, Result


class AnswerSerializer(serializers.ModelSerializer):
    """
    A serializer class for processing and validating answer data.

    This class is responsible for converting answer instances into formats that can
    be easily rendered into JSON or other content types, as well as validating
    incoming data for answers.

    Attributes:
        Some attribute descriptions may go here.

    Methods:
        serialize(): Converts an answer instance to a serializable format.
        validate(): Checks the validity of the incoming answer data.

    Attributes:
        answer_id: The unique identifier for the answer.
        content: The content of the answer provided by the user.
        created_at: The timestamp when the answer was created.
    """

    class Meta:
        model = Answer
        fields = ["id", "answer_text", "is_correct"]


class AnswerAllSerializer(serializers.ModelSerializer):
    """
    Serializer for handling answers in the application.

        This class is responsible for serializing and deserializing answer data,
        providing a structured format for data exchange between the client and
        server.

        Attributes:
            attribute1: Description of attribute1.
            attribute2: Description of attribute2.
            attribute3: Description of attribute3.

        Methods:
            method1: Description of method1.
            method2: Description of method2.
    """

    class Meta:
        model = Answer
        fields = ["id", "answer_text"]


class QuestionSerializer(serializers.ModelSerializer):
    """
    A serializer class for handling question data within the application.

    Attributes:
        answers: A list of answers associated with the question.

    Methods:
        (Add method names here if there are any)

    This class is responsible for serializing question-related data,
    providing a structured representation of questions and their associated answers.
    """

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "addition_info", "question_points", "answers"]


class QuestionAllAnswersSerializer(serializers.ModelSerializer):
    """
    Serializer for handling all answers related to a question.

    This class is designed to serialize data concerning all answers
    for a given question, providing a structured format for data
    exchange.

    Attributes:
        answers: A collection of answers associated with the question.

    Methods:
        (No methods defined in this class.)
    """

    answers = AnswerAllSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "addition_info", "question_points", "answers"]


class TestSerializer(serializers.ModelSerializer):
    """
    A class that handles the serialization of test data for easier manipulation and storage.

    Attributes:
        questions: A collection of questions to be serialized.

    Methods:
        (List of methods would go here if applicable)

    The TestSerializer class is designed to provide a structured way to manage and serialize test-related data,
    allowing for efficient data handling while maintaining clarity and organization.
    """

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = [
            "id",
            "author_id",
            "subject_id",
            "theme_id",
            "expert_id",
            "max_points",
            "questions",
        ]


class TestListSerializer(serializers.ModelSerializer):
    """
    A serializer class for handling list data in a test environment.

    This class provides functionality to serialize and deserialize lists of data,
    making it easier to manage data representation in tests.

    Methods:
        - serialize: Converts a list of data into a serialized format.
        - deserialize: Converts serialized data back into a list of data.

    Attributes:
        - data: Raw data to be serialized or deserialized.
        - format: The format in which the data will be serialized.

    The `serialize` method transforms the contained list data into a specified
    format, while the `deserialize` method takes serialized data and converts
    it back to the original list structure. The `data` attribute holds the list
    being processed, and the `format` attribute defines how that data is represented.
    """

    class Meta:
        model = Test
        fields = [
            "id",
            "author_id",
            "subject_id",
            "theme_id",
            "times_solved",
            "expert_id",
            "max_points",
        ]


class TestGetSerializer(serializers.ModelSerializer):
    """
    TestGetSerializer provides functionality for serializing test data.

        This class is responsible for handling the serialization of test data
        related to questions. It ensures that the data is structured properly
        for further processing or validation.

        Attributes:
            questions: A collection of questions to be serialized.

        Methods:
            (No methods defined in this class.)
    """

    questions = QuestionAllAnswersSerializer(many=True)

    class Meta:
        model = Test
        fields = [
            "id",
            "author_id",
            "subject_id",
            "theme_id",
            "expert_id",
            "max_points",
            "questions",
        ]


class CorrectAnswerSerializer(serializers.Serializer):
    """
    A serializer class for handling correct answer data associated with a question.

    Attributes:
        correct_answers: A list that holds the correct answers for the associated question.
        id_question: An identifier for the question to which the correct answers belong.

    Methods:
        (No defined methods)

    This class is primarily used to organize and serialize correct answer information.
    """

    correct_answers = serializers.ListField()
    id_question = serializers.IntegerField()


class TestUserSerializer(serializers.ModelSerializer):
    """
    Serializer for testing user data.

        This class is responsible for serializing user-related data in the context of testing.
        It facilitates the conversion of user objects into a format that can be easily rendered into
        JSON and vice versa, ensuring that the data meets the expected structure and validation
        required for testing purposes.

        Attributes:
            None

        Methods:
            None
    """

    class Meta:
        model = Result
        fields = "__all__"


class SolutionsSerializer(serializers.ModelSerializer):
    """
    Serializes solution data for API responses.

    This class is responsible for transforming solution objects into
    a format suitable for serialization, typically to JSON, for API
    communication.

    Methods:
        - serialize
        - deserialize

    Attributes:
        - solutions_list
        - version

    The `serialize` method converts solution objects into a standard
    format for output. The `deserialize` method takes serialized
    data and converts it back into solution objects. The `solutions_list`
    attribute holds the collection of solutions that are to be serialized,
    while the `version` attribute tracks the version of the serialization
    format being used.
    """

    class Meta:
        model = Solutions
        fields = ["id_question", "user_answer"]


class ResultsSerializer(serializers.ModelSerializer):
    """
    A serializer for processing results and converting them into a desired format.

    Attributes:
        solutions: A collection of solutions to be serialized.

    Methods:
        (Include method names here if applicable)

    This class is responsible for serializing results which may include
    various solutions. It provides a structured way to handle and output
    the data in a specific format.
    """

    solutions = SolutionsSerializer(many=True)

    class Meta:
        model = Result
        fields = [
            "id",
            "id_user",
            "id_test",
            "subject",
            "theme",
            "points_user",
            "solutions",
        ]


class SolutionsResultsSerializer(serializers.ModelSerializer):
    """
    Serialize the results of solutions for output in a specific format.

        This class is responsible for transforming solution results into a
        format suitable for consumption, typically in JSON or other serialized
        forms.

        Methods:
            None

        Attributes:
            None
    """

    class Meta:
        model = Solutions
        fields = "__all__"
