from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db import models


class RoleField(models.CharField):
    """
    A field representing a set of predefined role choices in a data model.

    Attributes:
        ROLE_CHOICES: A predefined set of choices available for the role field.

    Methods:
        __init__: Initializes a new instance of the class.

    The ROLE_CHOICES attribute defines the valid options that can be assigned
    to this field, ensuring that only specific roles can be used within the
    data model. The __init__ method sets up default values for the field's
    properties such as choices, maximum length, and validation requirements,
    ensuring proper initialization of the class.
    """

    ROLE_CHOICES = [
        ("student", "student"),
        ("teacher", "teacher"),
        ("admin", "admin"),
    ]

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the class.

            This method sets default values for certain keyword arguments
            related to choices, maximum length, and validation requirements,
            before calling the parent class's initializer.

            Args:
                *args: Variable length argument list for the parent class.
                **kwargs: Keyword arguments for the parent class which include:
                    - choices: A predefined set of role choices.
                    - max_length: The maximum length of the input, set to 7.
                    - blank: A boolean indicating if blank values are allowed, set to False.
                    - null: A boolean indicating if null values are allowed, set to False.

            Returns:
                None: This method does not return a value. It initializes the instance.
        """
        kwargs["choices"] = self.ROLE_CHOICES
        kwargs["max_length"] = 7
        kwargs["blank"] = False
        kwargs["null"] = False
        super().__init__(*args, **kwargs)


class UserManager(BaseUserManager):
    """
    Manages user accounts including creation of regular users and superusers.

    Methods:
        create_user: Creates and returns a user with an email, password, and name.
        create_superuser: Creates and returns a user with admin privileges.

    Attributes:
        None

    This class provides functionality to manage users effectively,
    allowing for the creation of both standard users and superusers
    with specific privileges.
    """

    def create_user(self, username, email, password, **extra_fields):
        """Создает и возвращает пользователя с имэйлом, паролем и именем."""
        if username is None:
            raise TypeError("Users must have a username.")

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(
            username=username, email=self.normalize_email(email), **extra_fields
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """Создает и возввращет пользователя с привилегиями суперадмина."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Representation of a User in the system.

        This class encapsulates all the necessary details of a user,
        including their authentication details and roles within the application.

        Attributes:
            username: The unique identifier for the user.
            email: The user's email address.
            is_active: Indicates whether the user account is active.
            is_staff: Indicates whether the user has staff privileges.
            is_superuser: Indicates whether the user has superuser privileges.
            created_at: The timestamp when the user account was created.
            updated_at: The timestamp when the user account was last updated.
            role: The role assigned to the user within the application.
            USERNAME_FIELD: The field used to identify the user.
            REQUIRED_FIELDS: A list of required fields for user creation.
            objects: The manager for the User model.

        Methods:
            __str__: Returns a string representation of the object for debugging and logging.
    """

    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = RoleField(default="student")

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        """
        Return a string representation of the object.

            This method is designed to provide a human-readable string that
            represents the current state of the object. It can be useful for
            debugging and logging purposes.

            Returns:
                A string that describes the object.
        """
        return self.email
