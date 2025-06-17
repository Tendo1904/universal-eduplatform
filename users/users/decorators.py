import jwt
from django.conf import settings
from rest_framework.response import Response
from functools import wraps
from rest_framework import status


def student_function(token):
    """
    Decodes a JSON Web Token (JWT) and checks if it belongs to a student.

        This function attempts to decode the provided JWT token using a secret key
        and verifies if the decoded token's role is 'student'. If successful,
        it returns a response indicating a valid student role. If the token is
        invalid or the role is not 'student', it returns an appropriate response
        with a failure message.

        Args:
            token: The JWT token to be decoded and validated.

        Returns:
            A Response object containing either a success status or a failure message.
    """
    try:
        token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        if token["role"] == "student":
            return Response(True)
    except Exception as e:
        return Response(
            {
                "Status": "Failed",
                "Message": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(False)


def student_access_only():
    """
    Decorator to restrict view access to student users only.

        This decorator checks if the user associated with the provided token
        is a student. If the user is not a student, it returns a response indicating
        the restriction. If the user is a student, it proceeds to execute the
        original view function.

        Args:
            view: The view function that needs to be decorated for student access.

        Returns:
            A wrapped view function that either denies access or allows the view to execute.
    """

    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not student_function(kwargs["token"]):
                return Response("You are not a student")
            return student_function(kwargs["token"])

        return _wrapped_view

    return decorator


def teacher_function(token):
    """
    Checks if the provided token belongs to a teacher.

        This function decodes a JWT token and verifies if the role specified
        in the token is 'teacher'. If successful, it returns a response indicating
        that the user is a teacher. In case of an error during decoding or if
        the role is not 'teacher', it returns an appropriate response.

        Args:
            token: The JWT token to be decoded and validated.

        Returns:
            A Response object indicating whether the user is a teacher
            (True) or not (False). In case of an error, a Response object
            with a failure message is returned.
    """
    try:
        token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        if token["role"] == "teacher":
            return Response(True)
    except Exception as e:
        return Response(
            {
                "Status": "Failed",
                "Message": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(False)


def teacher_access_only():
    """
    Decorator to restrict access to views for teachers only.

        This method returns a decorator that checks if the user associated
        with the provided token is a teacher. If the user is not a teacher,
        an appropriate response is returned. Otherwise, the original view
        function is executed.

        Args:
            view: The view function to be wrapped by the decorator.

        Returns:
            A wrapped view function that either restricts access or allows
            execution based on the user's teacher status.
    """

    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not teacher_function(kwargs["token"]):
                return Response("You are not a teacher")
            return teacher_function(kwargs["token"])

        return _wrapped_view

    return decorator


def admin_function(token):
    """
    Checks if the provided token corresponds to an admin user.

        This function decodes a JWT token to verify the user's role.
        If the token is valid and the user's role is 'admin', it returns a successful response.
        Otherwise, it returns a failure response with an error message.

        Args:
            token: The JWT token to be decoded and verified.

        Returns:
            A Response object indicating:
            - True if the token is valid and the role is 'admin'.
            - A failure message and status if the token is invalid or if the role is not 'admin'.
    """
    try:
        token = jwt.decode(token, key=settings.SECRET_KEY, algorithms=["HS256"])
        if token["role"] == "admin":
            return Response(True)
    except Exception as e:
        return Response(
            {
                "Status": "Failed",
                "Message": str(e),
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(False)


def admin_access_only():
    """
    Decorator to restrict access to admin users only.

        This decorator checks whether the user has admin privileges based on a token
        provided in the request's keyword arguments. If the user is not an admin,
        a response indicating lack of access is returned.

        Args:
            view: The view function to be wrapped by the decorator.

        Returns:
            A wrapped view function that enforces admin access rules.
    """

    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not admin_function(kwargs["token"]):
                return Response("You are not an admin")
            return admin_function(kwargs["token"])

        return _wrapped_view

    return decorator
