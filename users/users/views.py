from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    UserSerializer,
    LogoutSerializer,
    SignInSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .decorators import student_access_only, teacher_access_only, admin_access_only
import jwt
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema


def get_tokens_for_user(user):
    """
    Generate access and refresh tokens for a given user.

    This method creates a refresh token associated with the specified user and returns
    a dictionary containing both the refresh token and the associated access token.

    Args:
        user: The user for whom the tokens are to be generated.

    Returns:
        A dictionary containing:
            - 'refresh': The refresh token as a string.
            - 'access': The access token as a string.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginView(viewsets.ModelViewSet):
    """
    Handles user login and authentication in the application.

    This class manages the login process for users, ensuring that
    credentials are validated and that authentication tokens are
    generated upon successful login.

    Attributes:
        serializer_class: The serializer class used for validating
                          and deserializing the login credentials.
        LoginSerializer: A specific implementation of the serializer
                         for handling login data.

    Methods:
        post: Handles user login and generates authentication tokens.
    """

    serializer_class = LoginSerializer

    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: SignInSerializer}
    )
    def post(self, request, format=None):
        """
        Handles user login and generates authentication tokens.

            This method processes a login request by authenticating the user with
            the provided username and password. If the credentials are valid and
            the account is active, it generates access and refresh tokens, sets
            them as cookies in the response, and returns the user's information.
            If the account is not active or the credentials are invalid, it
            returns an appropriate error message.

            Args:
                request: The HTTP request containing the login credentials,
                         specifically the username and password in the request data.
                format: An optional format parameter.

            Returns:
                A Response object containing the user's details or an error
                message along with the status code.
        """
        data = request.data
        response = Response()
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.set_cookie(
                    key="refresh_token",
                    value=data["refresh"],
                    expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                response.data = list(
                    User.objects.filter(username=request.data["username"]).values(
                        "id", "username", "email", "role", "is_active"
                    )
                )
                return response
            else:
                return Response(
                    {"No active": "This account is not active"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid username or password"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RegistrationAPIView(generics.CreateAPIView):
    """
    Handles user registration through an API interface.

    This class provides the functionality to register new users by processing
    incoming registration requests and returning appropriate responses.

    Attributes:
        permission_classes: Defines the permissions required to access the API.
        serializer_class: The serializer class used to validate and serialize user data.
        RegistrationSerializer: The specific serializer implementation for user registration.

    Methods:
        (If applicable, list methods here)

    The methods of this class facilitate the handling of registration requests
    and ensure that user data is correctly validated and processed. The attributes
    define the necessary configurations for permissions and data serialization.
    """

    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


class UserAPIView(viewsets.ModelViewSet):
    """
    Handles user-related API requests, catering specifically to
    different user roles in an educational setting (admin, teacher,
    student).

    Methods:
        admin
        teacher
        student

    Attributes:
        permission_classes
        serializer_class
        UserSerializer
        queryset
        User

    The class includes methods for processing requests based on user
    roles, ensuring that each request is handled according to the
    permissions assigned to that role. The `admin` method is designed
    for admin users, the `teacher` method is for authorized teachers,
    and the `student` method is for student-specific requests. The
    attributes define the serialization and querying behaviors required
    for handling user data.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User

    @admin_access_only()
    def admin(self, request, *args, **kwargs):
        """
        Handles admin requests and returns a response.

            This method is restricted to admin users only. It processes the request
            and returns a positive response indicating success.

            Args:
                request: The HTTP request object containing data for processing.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                A Response object indicating success (True).
        """
        return Response(True)

    @teacher_access_only()
    def teacher(self, request, *args, **kwargs):
        """
        Handles requests exclusive to authorized teachers.

            This method processes incoming requests that can only be accessed by users
            with teacher privileges. It returns a response indicating the success
            of the operation.

            Args:
                request: The HTTP request object containing data about the request.
                *args: Additional positional arguments for flexibility.
                **kwargs: Additional keyword arguments for flexibility.

            Returns:
                Response: A response indicating success as a boolean.
        """
        return Response(True)

    @student_access_only()
    def student(self, request, *args, **kwargs):
        """
        Handles student-specific requests.

            This method processes a request intended for student access and returns
            a response indicating the success of the operation.

            Args:
                request: The HTTP request object containing data for the operation.
                *args: Additional positional arguments for extended functionality.
                **kwargs: Additional keyword arguments for extended functionality.

            Returns:
                A Response object indicating success.
        """
        return Response(True)


class LogoutAPIView(generics.GenericAPIView):
    """
    Handles user logout operations by processing POST requests to invalidate
    user sessions.

    Attributes:
        serializer_class: The serializer class to be used for validating
            logout data.
        LogoutSerializer: Specifies the serializer responsible for
            handling logout data.
        permission_classes: Defines the permission classes that
            determine if the request is authorized.

    Methods:
        post: Handles POST requests by validating and saving the
            provided data.
    """

    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Handles POST requests by validating and saving the provided data.

            This method processes incoming POST requests, validating the data
            using the specified serializer class, and saves the data if valid.
            Upon successful processing, it returns an HTTP 204 No Content response.

            Args:
                request: The HTTP request object containing the data to be processed.

            Returns:
                An HTTP response with a status code indicating the result of
                the operation; specifically, an HTTP 204 No Content status
                when the operation is successful.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenDecode(viewsets.ViewSet):
    """
    A class to decode JSON Web Tokens (JWT).

    This class provides functionality to decode a JWT and handle
    responses based on the validity of the token. It is designed to
    facilitate the secure handling of JWTs in web applications.

    Methods:
        decode: Decodes a JSON Web Token (JWT) and returns the corresponding response.

    Attributes:
        None

    The `decode` method attempts to decode a JWT provided in the
    keyword arguments. If the decoding is successful, it returns
    the decoded token in the response with a 200 OK status. If the
    token is expired or invalid, it returns an appropriate error
    message with a 401 Unauthorized status.
    """

    def decode(self, request, *args, **kwargs):
        """
        Decode a JSON Web Token (JWT) and return the corresponding response.

            This method attempts to decode a JWT provided in the kwargs. If successful,
            it returns the decoded token in the response with a 200 OK status. If the
            token has expired or is invalid, it returns an appropriate error message
            with a 401 Unauthorized status.

            Args:
                request: The HTTP request object.
                *args: Additional positional arguments.
                **kwargs: Keyword arguments, which must include 'token', the JWT to decode.

            Returns:
                A Response object containing either the decoded token or an error message.
        """
        try:
            token = jwt.decode(
                kwargs["token"], key=settings.SECRET_KEY, algorithms=["HS256"]
            )
            return Response(token, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Token has expired"}, status=status.HTTP_401_UNAUTHORIZED
            )
        except jwt.InvalidTokenError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )
