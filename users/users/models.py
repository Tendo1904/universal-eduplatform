from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

from django.db import models

class RoleField(models.CharField):
    """
    This class represents a custom field for storing user role information.
    
        Class Attributes:
        - ROLE_CHOICES: A list of tuples representing the available choices for user roles.
    
        Class Methods:
        - __init__: Initializes the RoleField with specified choices for user roles.
    """

    ROLE_CHOICES = [
        ('student', 'student'),
        ('teacher', 'teacher'),
        ('admin', 'admin'),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the class with predefined choices, max_length, blank, and null settings.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            None
        """
        kwargs['choices'] = self.ROLE_CHOICES
        kwargs['max_length'] = 7
        kwargs['blank'] = False
        kwargs['null'] = False
        super().__init__(*args, **kwargs)


class UserManager(BaseUserManager):
    """
    Class representing a user manager that facilitates creating and managing user accounts.
    
        Class Attributes:
        - users: A dictionary storing user objects with user IDs as keys.
    
        Methods:
        - create_user: Creates and returns a user with email, password, and name.
        - create_superuser: Creates and returns a user with super admin privileges.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates and returns a user with an email, password, and username.
        
        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields to be included when creating the user.
        
        Returns:
            User: The user object created with the provided details.
        """
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and returns a user with superadmin privileges.
        
        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The password for the user.
            **extra_fields: Additional fields for the user, e.g., is_staff, is_superuser, is_active, and role.
        
        Returns:
            User: An instance of the user with superadmin privileges.
        """
        extra_fields.setdefault('is_staff', True) 
        extra_fields.setdefault('is_superuser', True) 
        extra_fields.setdefault('is_active', True) 
        extra_fields.setdefault('role', 'admin') 
 
        if extra_fields.get('is_staff') is not True: 
            raise ValueError('Superuser must have is_staff=True.') 
        if extra_fields.get('is_superuser') is not True: 
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields) 

class User(AbstractBaseUser, PermissionsMixin):
    """
    This class represents a user in the system with various attributes and methods for user management.
    
        Class Attributes:
        - username: The username of the user.
        - email: The email address of the user.
        - is_active: Indicates whether the user is active or not.
        - is_staff: Indicates whether the user is a staff member or not.
        - is_superuser: Indicates whether the user has superuser privileges.
        - created_at: The timestamp of when the user account was created.
        - updated_at: The timestamp of when the user account was last updated.
        - role: Role assigned to the user.
        - USERNAME_FIELD: The field used for identifying a user (usually 'username').
        - REQUIRED_FIELDS: The list of fields required to create a user.
        - objects: The manager for handling user queries.
    
        Class Methods:
        - __str__: Returns a string representation of the user object.
    """

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = RoleField(default='student')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        """
        Return the email address of the object as a string representation.
        
        Args: 
            self: the instance of the object to be converted to a string.
        
        Returns: 
            str: The email address of the object.
        """
        return self.email
