from rest_framework import serializers
from .models import Test, Question, Solutions, Answer, Result


class AnswerSerializer(serializers.ModelSerializer):
    """
    A class for serializing Answer objects, providing methods to convert Answer objects into JSON format.
    
        Attributes:
            answer_text: The text of the answer.
            is_correct: A boolean indicating whether the answer is correct or not.
            question: The question related to the answer.
    
        Methods:
            serialize_answer: Converts the Answer object into a dictionary ready to be serialized to JSON.
            deserialize_answer: Converts a dictionary back to an Answer object.
    """

    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct']

class AnswerAllSerializer(serializers.ModelSerializer):
    """
    A serializer class to handle data serialization for answering all questions.
    
        Attributes:
            question (str): The question to be answered.
            answer (str): The answer to the question.
    
        Methods:
            - serialize_data(): Serialize data for the given question and answer.
            - validate_data(): Validate the provided question and answer.
    """

    class Meta:
        model = Answer
        fields = ['id', 'answer_text']

class QuestionSerializer(serializers.ModelSerializer):
    """
    This class provides functionality to serialize and deserialize question data for a questionnaire application.
    
        Class Attributes:
        - answers
    """

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text','addition_info', 'question_points', 'answers']

class QuestionAllAnswersSerializer(serializers.ModelSerializer):
    """
    This class provides a serializer for handling all answers related to a question.
    
        Class Attributes:
        - answers: A list of all answers related to the question.
    
        Methods:
        - serialize_answers: Serializes all answers related to the question.
        - deserialize_answers: Deserializes all answers related to the question.
    """

    answers = AnswerAllSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text','addition_info', 'question_points', 'answers']

class TestSerializer(serializers.ModelSerializer):
    """
    This class provides functionality for serializing test data.
    
        Attributes:
        - questions: A list of questions to be serialized.
    """

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'author_id', 'subject_id', 'theme_id', 'expert_id', 'max_points', 'questions']


class TestListSerializer(serializers.ModelSerializer):
    """
    A class for serializing lists in a specific format.
    
        Attributes:
        - delimiter: The delimiter used to separate elements in the serialized list.
    
        Methods:
        - serialize: Serializes a list into a string using the specified delimiter.
        - deserialize: Deserializes a string into a list using the specified delimiter.
    """

    class Meta:
        model = Test
        fields = ['id', 'author_id', 'subject_id', 'theme_id', 'times_solved', 'expert_id', 'max_points']


class TestGetSerializer(serializers.ModelSerializer):
    """
    This class represents a serializer for retrieving test data.
    
        Class Attributes:
        - serializer: The serializer for retrieving test data from the database.
    
        The TestGetSerializer class provides methods for retrieving test data from the database.
    """

    questions = QuestionAllAnswersSerializer(many=True)

    class Meta:
        model = Test
        fields = ['id', 'author_id', 'subject_id', 'theme_id', 'expert_id', 'max_points', 'questions']


class CorrectAnswerSerializer(serializers.Serializer):
    """
    This class provides serialization for correct answer objects.
    
        Class Attributes:
        - correct_answers: The correct answers stored in the serializer.
        - id_question: The identifier of the question associated with the correct answer.
    """

    correct_answers = serializers.ListField()
    id_question = serializers.IntegerField()

class TestUserSerializer(serializers.ModelSerializer):
    """
    Class representing a user serializer for transforming user data into JSON format.
    
        Methods:
        - serialize_user: Serializes user data into a JSON object.
    
        Attributes:
        - user: The user object to be serialized.
        - fields: The fields to include in the serialized user data.
    
        The TestUserSerializer class provides functionality to serialize user data into a JSON format. It includes a method to perform the serialization and attributes to configure the serialization process.
    """

    class Meta:
        model = Result
        fields = "__all__"

class SolutionsSerializer(serializers.ModelSerializer):
    """
    Class to serialize and deserialize solutions data.
    
        Attributes:
            solutions_list: A list of solutions data.
            version: Version number of the solutions data.
    
        Methods:
            serialize(): Serializes the solutions data.
            deserialize(): Deserializes the solutions data.
    """

    class Meta:
        model = Solutions
        fields = ['id_question', 'user_answer']

class ResultsSerializer(serializers.ModelSerializer):
    """
    This class provides serialization functionality for storing and retrieving results data.
    
        Class Attributes:
        - solutions: A list of solutions generated during processing.
    """

    solutions = SolutionsSerializer(many=True)
    class Meta:
        model = Result
        fields = ['id', 'id_user', 'id_test', 'subject', 'theme', 'points_user', 'solutions']

class SolutionsResultsSerializer(serializers.ModelSerializer):
    """
    This class provides a serializer for the results of SolutionsProvider to be used for storage or exchange.
    
        Attributes:
            data (list): A list containing the results data to be serialized.
            format (str): The desired format for the serialization output.
    
        Methods:
            serialize(): Convert the results data into the specified format for serialization.
    """

    class Meta:
            model = Solutions
            fields = "__all__"


