import jwt
from django.conf import settings 
from rest_framework.response import Response
from functools import wraps
from rest_framework import status

def student_function(token):
    """
    Check if the given token is valid for a student role.
    
    Parameters:
    - token: a string representing the authentication token
    
    Returns:
    - Response: True if the token is valid for a student, False otherwise
    
    Args:
    - token (str): a string representing the authentication token
    
    Return:
    - Response: True if the token is valid for a student, False otherwise
    """
    try:
        token = jwt.decode(token,
                            key=settings.SECRET_KEY,
                            algorithms=["HS256"])
        if token['role'] == 'student':
            return Response(True)
    except Exception as e:
        return Response({
            'Status': 'Failed',
            'Message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response(False)


def student_access_only():
    """
    A decorator function that restricts access to views based on whether the user has student privileges.
    
    Args:
        - view: The view function to be decorated.
    
    Returns:
        A decorated function that checks the user's token to verify if they have student access. If not, it returns a Response with the message "You are not a student".
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not student_function(kwargs['token']):
                return Response("You are not a student")
            return student_function(kwargs['token'])
        return _wrapped_view
    return decorator

def teacher_function(token):
    """
    teacher_function
    
    Decodes a JWT token, checks if the token represents a teacher, and returns True if it does, False otherwise. If an error occurs during decoding or validation, a Response object with failure details is returned.
    
    Args:
    - token: The JWT token to be decoded and analyzed.
    
    Returns:
    - Response: True if the token represents a teacher, False otherwise. If an error occurs during decoding or validation, a Response object with failure details is returned.
    """
    try:
        token = jwt.decode(token,
                            key=settings.SECRET_KEY,
                            algorithms=["HS256"])
        if token['role'] == 'teacher':
            return Response(True)
    except Exception as e:
        return Response({
            'Status': 'Failed',
            'Message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response(False)


def teacher_access_only():
    """
    Decorator that restricts access to views to only teachers.
        
        Parameters:
        - view: The view function to be restricted.
        - request: The HTTP request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.
        
        Returns:
        - A decorator function that limits access to the view function to only teachers.
        - The view function, if the user has teacher access rights; otherwise, a response indicating the user is not a teacher.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not teacher_function(kwargs['token']):
                return Response("You are not a teacher")
            return teacher_function(kwargs['token'])
        return _wrapped_view
    return decorator

def admin_function(token):
    """
    Verify the provided token for admin role permissions and return a Response object with a boolean value based on admin role validation.
    
    Args:
        token (str): A string representing the token to be decoded and validated.
    
    Returns:
        Response: Response object containing a boolean value indicating if the token has admin role permissions.
    """
    try:
        token = jwt.decode(token,
                            key=settings.SECRET_KEY,
                            algorithms=["HS256"])
        if token['role'] == 'admin':
            return Response(True)
    except Exception as e:
        return Response({
            'Status': 'Failed',
            'Message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)
    return Response(False)


def admin_access_only():
    """
    Summary:
        Restricts access to a view function to only users with admin privileges.
    
    Description:
        The method `admin_access_only` serves as a decorator that validates if the user possesses admin rights by utilizing the `admin_function` with the token obtained from the view function's keyword arguments. If the user lacks admin privileges, it responds with a message indicating restricted access.
    
    Parameters:
        - No parameters.
        
    Args:
        view: The view function to be restricted based on admin privileges.
    
    Return:
        A decorator function that restricts access to the wrapped view function according to the admin privileges.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not admin_function(kwargs['token']):
                return Response("You are not an admin")
            return admin_function(kwargs['token'])
        return _wrapped_view
    return decorator