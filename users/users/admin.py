from django.contrib import admin
from .models import User

@admin.register(User)
class TestAdmin(admin.ModelAdmin):
    """
    This class represents the TestAdmin functionality for managing test-related data.
    
        Class Attributes:
        - list_display
    
        The TestAdmin class includes methods for managing tests such as creating, updating, and deleting tests.
    """

    list_display = ('id', 'email', 'username', 'role', 'is_active' , 'is_staff', 'is_superuser', 'created_at', 'updated_at')
