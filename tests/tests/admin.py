from django.contrib import admin

from .models import Question, Test, Answer, Result, Solutions

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """
    Class TestAdmin represents an entity that handles administrative tasks related to testing.
    
        Class Methods:
        - run_test: Runs a test on the system.
        - create_test_case: Creates a new test case for the system.
    
        Attributes:
        - test_cases: A list of test cases stored in the system.
    
        The TestAdmin class provides functionalities to manage and run tests efficiently within the system.
    """

    list_display = ('author_id', 'subject_id', 'theme_id', 'times_solved' , 'expert_id', 'max_points')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Class QuestionAdmin is a custom admin panel for managing questions in a questionnaire application.
    
        Attributes:
        - list_display: List of attributes to display in the admin panel for each question.
    
        Methods:
        - save_model(): Overrides the save_model method in the admin interface to add custom behavior when saving a question.
        - delete_model: Overrides the delete_model method in the admin interface to add custom behavior when deleting a question.
    """



    list_display = ('id_test', 'question_text', 'addition_info', 'question_points')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Class AnswerAdmin is a custom admin panel for managing answers in the application.
    
        Class Attributes:
        - list_display
    """

    list_display = ('id_question', 'answer_text', 'is_correct')

@admin.register(Result)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'id_test', 'points_user')

@admin.register(Solutions)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id_result', 'id_question', 'user_answer' )
