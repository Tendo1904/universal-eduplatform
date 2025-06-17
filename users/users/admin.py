from django.contrib import admin
from .models import User


@admin.register(User)
class TestAdmin(admin.ModelAdmin):
    """
    A class that manages the administration interface for tests.

    Attributes:
        list_display: A list that defines which fields will be displayed in the admin interface.

    Methods:
        (No methods defined in this class)

    The TestAdmin class is used to customize and control the display of test-related information
    in an administrative context. The class attribute list_display determines which attributes
    of the test instances are shown within the admin interface, allowing for easier management
    and overview of test data.
    """

    list_display = (
        "id",
        "email",
        "username",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "created_at",
        "updated_at",
    )
