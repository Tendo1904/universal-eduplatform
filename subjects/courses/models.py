from django.db import models

class Subject(models.Model): #Таблица с данными предметов
    name_subject = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns the string representation of the object.
        
        Args:
            self: The object itself.
        
        Returns:
            str: The value of the 'name_subject' attribute of the object.
        """
        return self.name_subject

class Theme(models.Model): #Таблица с темами тестов
    name_theme = models.CharField(max_length=100)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the name theme.
        
        Args:        
        - self (Theme): An instance of the Theme class.
        
        Returns:
        - str: The name theme of the instance.
        """
        return self.name_theme

class Course(models.Model):
    """
    Class representing a Course, containing information about a particular educational course.
    
        Class Methods:
        - __str__: Returns a string representation of the Course object.
    
        Class Attributes:
        - name_course
        - id_subject
        - id_expert
        - description
    """

    name_course = models.CharField(max_length=100)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    id_expert = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the course object.
                
                Parameters:
                    self: The course object itself.
                
                Returns:
                    str: The name of the course.
        """
        return self.name_course

class Student_Course_Subject(models.Model):
    """
    This class represents a student's enrollment in a particular course subject. It tracks the student, course, and subject details.
    
        Class Attributes:
        - id_student: The unique identifier of the student.
        - id_subject: The unique identifier of the subject.
        - id_expert: The unique identifier of the expert.
    """

    id_student = models.IntegerField(null=True, blank=True)
    id_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='course_id_subject')
    id_expert = models.IntegerField(null=True, blank=True)

    # def __str__(self):
    #     return self.id_expert
