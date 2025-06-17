from django.contrib import admin

from .models import Question, Test, Answer, Result, Solutions


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """

    TestAdmin is a class that handles administrative functionalities for test management.

    Attributes:
        list_display: A configuration attribute for specifying the display options of test items.

    Methods:
        (No methods are defined in this class)

    The class primarily serves to manage the presentation and configuration of test-related data
    in an administrative context, focusing on what information should be displayed to users.
    """

    list_display = (
        "author_id",
        "subject_id",
        "theme_id",
        "times_solved",
        "expert_id",
        "max_points",
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing questions within the application.

        This class provides an interface to manage questions in the admin panel,
        allowing for customization of how questions are displayed and handled.

        Attributes:
            list_display: A list of attributes to be displayed in the admin panel.

        Methods:
            (No methods are defined in this class.)
    """

    list_display = ("id_test", "question_text", "addition_info", "question_points")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Answer objects.

        This class is responsible for the administration of Answer instances, providing
        necessary configurations for how they should be displayed in the admin panel.

        Attributes:
            list_display: A configuration for the fields to be displayed in the admin list view.

    """

    list_display = ("id_question", "answer_text", "is_correct")


@admin.register(Result)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing question objects.

    This class provides an interface for displaying and managing
    question objects within an admin panel, allowing for configuration
    of how questions are listed and presented.

    Attributes:
        list_display: A list of fields to display in the admin interface.

    Methods:
        (No specific methods are defined in this class.)
    """

    list_display = ("id_user", "id_test", "points_user")


@admin.register(Solutions)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing questions in the application.

        This class is responsible for configuring the admin panel's display
        related to questions, facilitating the management and organization
        of question objects.

        Attributes:
            list_display: A list that defines which fields are displayed
                          in the admin list view for questions.

    """

    list_display = ("id_result", "id_question", "user_answer")
