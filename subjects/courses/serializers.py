from rest_framework import serializers
from .models import *


class SubjectSerializer(serializers.ModelSerializer):
    """
    A serializer class for converting Subject instances to and from various data formats.

    Methods:
        serialize: Converts a Subject instance to a JSON-compatible representation.
        deserialize: Creates a Subject instance from a JSON representation.

    Attributes:
        fields: A list of the fields in the Subject model that will be serialized.
        validation_errors: A list to hold any validation errors encountered during serialization.

    This class is responsible for transforming Subject objects into formats suitable for
    data transfer and storage, and vice versa. The methods handle the conversion process
    while ensuring that the data adheres to the specified structure and validation rules.
    """

    class Meta:
        model = Subject
        fields = "__all__"


class ThemeSerializer(serializers.ModelSerializer):
    """
    Serializes theme data for processing and representation.

        This class is responsible for converting theme-related data into a format suitable for storage or transmission.
        It may include functionality for validating and transforming input data, ensuring that the output adheres to expected formats.

        Attributes:
            themes: A collection of theme data to be serialized.

        Methods:
            serialize: Converts the theme data into a specific output format.
            validate: Checks the validity of the theme data before serialization.
    """

    class Meta:
        model = Theme
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for processing Course data.

    This class is responsible for converting Course instances into a format
    suitable for consumption by clients, typically in JSON format. It helps
    streamline the data exchange process between the server and clients.

    Attributes:
        - <attribute_1>: Description of attribute 1.
        - <attribute_2>: Description of attribute 2.
        - ...

    Methods:
        - <method_1>
        - <method_2>
        - ...

    The attributes facilitate various aspects of the serialization
    process, while the methods define the logic needed to serialize
    and possibly validate Course instances.
    """

    class Meta:
        model = Course
        fields = "__all__"


class Student_Course_SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer for handling serialization and deserialization of student, course, and subject data.

    This class is responsible for converting complex data types related to students, courses, and subjects
    into JSON format and vice versa, facilitating easier data exchange and presentation in APIs.

    Attributes:
        None

    Methods:
        None
    """

    class Meta:
        model = Student_Course_Subject
        fields = "__all__"
