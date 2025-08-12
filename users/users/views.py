from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer, LogoutSerializer, SignInSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .decorators import (
    student_access_only,
    teacher_access_only,
    admin_access_only
)
import jwt
from django.conf import settings 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema

def get_tokens_for_user(user):
    """
    Retrieve tokens for a given user.
    
    Parameters:
        user: The user object for which tokens are to be retrieved.
    
    Returns:
        dict: A dictionary containing the user's refresh and access tokens.
        
    Args:
        user (object): The user object for which tokens are to be retrieved.
    
    Return:
        dict: A dictionary containing the user's refresh and access tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(viewsets.ModelViewSet):
    """
    Class representing a view for handling user login functionality.
    
        Class Attributes:
        - serializer_class: The serializer class used for validating and deserializing login data.
        - LoginSerializer: The specific serializer class for handling user login data.
    
        Class Methods:
        - post: Handles the HTTP POST request for user login, validating the login data and authenticating the user.
    """

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer,
        responses={200: SignInSerializer})
    def post(self, request, format=None):
        """
        Post method to authenticate user credentials and generate tokens for authentication.
            
            Parameters:
            - self: The instance of the class.
            - request: HTTP request object containing user authentication details.
            
            Returns:
            - Response object containing user data and tokens if authentication is successful.
            - Response object with error message if authentication fails.
            - Response object containing user data (id, username, email, role, is_active) if authentication is successful.
            - Response object with error message if authentication fails.
        """
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.set_cookie(
                    key='refresh_token',
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                    httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                )
                response.data = list(User.objects.filter(username=request.data['username']).values('id', 'username', 'email', 'role', 'is_active'))
                return response
            else:
                return Response({"No active": "This account is not active"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password"}, status=status.HTTP_404_NOT_FOUND)
    
class RegistrationAPIView(generics.CreateAPIView):
    """
    Class to handle registration endpoint API functionality.
    
        Class Attributes:
        - permission_classes
        - serializer_class
        - RegistrationSerializer
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

class UserAPIView(viewsets.ModelViewSet):
    """
    This class defines a REST API view for handling user-related operations.
        It includes methods for managing user data through HTTP requests.
    
        Class Attributes:
        - permission_classes: Determines the permissions required to access the API endpoints.
        - serializer_class: Defines the serializer to use for user data serialization.
        - UserSerializer: The serializer class used for transforming user data.
        - queryset: Represents the queryset used to retrieve user data from the database.
        - User: Refers to the User model class representing users in the system.
    
        Class Methods:
        - admin: Handles admin-related operations for users.
        - teacher: Manages teacher-specific actions for users.
        - student: Deals with student-related functionalities for users.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User
    
    @admin_access_only()
    def admin(self, request, *args, **kwargs):
        """
        Summary:
                    Validates admin access for the Universal EduPlatform AI Module and returns a response.
                
                Parameters:
                    self: Instance of the UserAPIView class.
                    request: Information related to the request.
                    *args: Additional positional arguments.
                    **kwargs: Additional keyword arguments.
                
                Returns:
                    Response: A boolean value indicating whether the user has admin access for the Universal EduPlatform AI Module or not.
        """
        return Response(True)

    @teacher_access_only()
    def teacher(self, request, *args, **kwargs):
        """
        Processes the teacher request and determines if the request is from a teacher.
        
        Args:
            self: the instance of the class
            request: the incoming request object
        
        Returns:
            bool: Whether the request is from a teacher or not
        """
        return Response(True)
    
    @student_access_only()
    def student(self, request, *args, **kwargs):
        """
        Retrieves information about a student.
        
        Args:
         - request: The request object containing the student details.
        
        Returns:
         - Response: A response object indicating if the student information was successfully retrieved.
        """
        return Response(True)

class LogoutAPIView(generics.GenericAPIView):
    """
    Class representing a view for handling user logout requests.
    
        Class Methods:
        - post: Handles the HTTP POST request for logging out the user.
    """

    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Performs a POST request to create a new object based on the provided data.
        
        Parameters:
        - self: the instance of the class.
        - request: the request object containing data to be serialized and saved.
        
        Returns:
        A Response object with a status code of HTTP 204 NO CONTENT.
        
        Args:
        - request: The request object containing data to be serialized and saved.
        
        Return:
        A Response object with a status code of HTTP 204 NO CONTENT.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TokenDecode(viewsets.ViewSet):
    """
    Class to decode tokens for authentication purposes.
    
        Class Methods:
        - decode: Decodes the token for authentication.
    """

    def decode(self, request, *args, **kwargs):
        """
        Decode a JWT token provided in the request kwargs.
        
        Args:
            self: The object instance.
            request: The HTTP request object containing the token in kwargs.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            Response: A response object containing the JWT token payload or an error message.
        """
        try:
            token = jwt.decode(kwargs['token'],
                                key=settings.SECRET_KEY,
                                algorithms=["HS256"])
            return Response(token, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
