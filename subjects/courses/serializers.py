from rest_framework import serializers
from .models  import*

class SubjectSerializer(serializers.ModelSerializer):
    """
    This class provides functionality to serialize and deserialize subject objects.
    
        Attributes:
        - subject_name: The name of the subject.
        - subject_code: The code of the subject.
    
        Methods:
        - serialize_subject: Serializes a subject object into a dictionary.
        - deserialize_subject: Deserializes a dictionary into a subject object.
    """

    class Meta():
        model = Subject
        fields = "__all__"

class ThemeSerializer(serializers.ModelSerializer):
    """
    This class provides a serializer for themes, allowing serialization and deserialization of theme data.
        Attributes:
        - theme_name: The name of the theme.
        - theme_colors: The colors associated with the theme.
        - theme_settings: The settings defined for the theme.
    """

    class Meta():
        model = Theme
        fields = "__all__"

class CourseSerializer(serializers.ModelSerializer):
    """
    This class CourseSerializer provides methods to serialize course objects and attributes.
    
        Attributes:
            course_id: A unique identifier for the course.
            course_name: The name of the course.
            course_description: A short description of the course.
    
        Methods:
            serialize_course: Serializes the course object into a dictionary.
            deserialize_course: Deserializes a dictionary into a course object.
    """

    class Meta():
        model = Course
        fields = "__all__"

class Student_Course_SubjectSerializer(serializers.ModelSerializer):
    """
    Serializer class for Student Course Subject model that helps serialize and deserialize data for CRUD operations.
    
        Attributes:
            attributes: A dictionary of attributes for the Student Course Subject model.
            properties: A list of properties for the Student Course Subject model.
            class fields: A list of class fields for the Student Course Subject model.
    
        Methods:
            serialize(): Serializes the data for the Student Course Subject model.
            deserialize(): Deserializes the data for the Student Course Subject model.
    """

    class Meta():
        model = Student_Course_Subject
        fields = "__all__"