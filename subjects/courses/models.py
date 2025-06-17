from django.db import models


class Subject(models.Model):  # Таблица с данными предметов
    name_subject = models.CharField(max_length=100)

    def __str__(self):
        """
        Return a string representation of the object.

            This method returns the name of the subject associated with the object.

            Returns:
                The name of the subject as a string.
        """
        return self.name_subject


class Theme(models.Model):  # Таблица с темами тестов
    name_theme = models.CharField(max_length=100)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the Course object.

            This method returns a human-readable string that represents
            the Course instance, typically the name of the course.

            Returns:
                A string that represents the name of the course.
        """
        return self.name_theme


class Course(models.Model):
    """
    Represents a course with associated details for a specific subject and expert.

    Attributes:
        name_course: The name of the course.
        id_subject: The identifier for the subject associated with the course.
        id_expert: The identifier for the expert teaching the course.
        description: A brief description of the course content.

    Methods:
        __str__: Returns a string representation of the Course instance.

    The Course class encapsulates information about a specific curriculum offering,
    including its title, subject, instructor, and a description. The __str__ method
    provides a user-friendly string representation of the Course object, making it
    easier to display course information.
    """

    name_course = models.CharField(max_length=100)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    id_expert = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        Return a string representation of the Student_Course_Subject instance.

            This method generates a human-readable string that describes
            the Student_Course_Subject object, typically used for display
            purposes.

            Returns:
                A string that represents the Student_Course_Subject instance.
        """
        return self.name_course


class Student_Course_Subject(models.Model):
    """
    Represents the relationship between a student, a subject, and an expert.

        This class manages the association of students with their subjects and the experts
        overseeing those subjects. It is designed to facilitate educational tracking and management.

        Attributes:
            id_student: The unique identifier for the student.
            id_subject: The unique identifier for the subject.
            id_expert: The unique identifier for the expert associated with the subject.

        Methods:
            (no methods are defined in this class)
    """

    id_student = models.IntegerField(null=True, blank=True)
    id_subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="course_id_subject"
    )
    id_expert = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.id_expert
