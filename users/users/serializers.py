from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _


class LoginSerializer(TokenObtainPairSerializer):
    """
    A serializer class for handling user login and token generation.

    This class is responsible for serializing user login data and generating
    authentication tokens with custom claims for the authenticated users.

    Methods:
        get_token: Generates a token for the specified user with custom claims.

    Attributes:
        (No attributes defined in this class)

    The get_token method retrieves a token for a given user and includes
    custom claims such as the user's username and role in the token data.
    """

    def get_token(self, user):
        """
        Generates a token for the specified user with custom claims.

            This method retrieves a token for the given user and adds custom claims
            such as the user's username and role to the token.

            Args:
                user: The user for whom the token is being generated. This user
                object should contain attributes like username and role.

            Returns:
                A dictionary representing the token, which includes the standard
                token data along with the custom claims for username and role.
        """
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["role"] = user.role

        return token


class SignInSerializer(serializers.ModelSerializer):
    """
    Serializer class for handling user sign-in data.

        This class is responsible for validating and serializing the data
        provided during the user sign-in process.

        Methods:
            - validate_data: Validates the sign-in data.
            - create: Creates a sign-in session for the user.

        Attributes:
            - username: The username of the user attempting to sign in.
            - password: The password of the user attempting to sign in.

        The `validate_data` method ensures that the provided credentials
        meet the necessary requirements for sign-in. The `create` method
        initiates the sign-in process by creating a session for the user
        upon successful validation. The `username` and `password` attributes
        hold the user's provided credentials for authentication purposes.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "is_active"]


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer class for user registration.

    This class handles the serialization and deserialization of user
    data, facilitating the creation of new user instances within
    the application. It ensures that data is correctly validated and
    processed for user registration.

    Attributes:
        password: The password attribute to hold the user's password.

    Methods:
        create: Create a new user instance in the database using the
        provided validated data.
    """

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    @classmethod
    def create(self, validated_data):
        """
        Create a new user.

                This method creates a new user instance in the database using the
                provided validated data. It encapsulates the logic of creating
                a user while ensuring that the data passed in is valid.

                Args:
                    validated_data: A dictionary containing the validated user
                    information required to create a new user.

                Returns:
                    The newly created user instance.
        """
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data.

    This class is responsible for converting user data to and from various formats.

    Attributes:
        - user_data: The data associated with the user to be serialized or deserialized.

    Methods:
        - serialize: Converts user data to a desired format.
        - deserialize: Converts data from a desired format back to user data.

    The `serialize` method transforms user information into a format suitable for storage or transmission.
    The `deserialize` method takes formatted data and converts it back into a user object representation.
    """

    class Meta:
        model = User
        fields = ["id", "email", "username", "role"]


class LogoutSerializer(serializers.Serializer):
    """
    Serializer for handling user logout functionality.

    This class is responsible for validating the refresh token provided by
    the user and performing the logout operation by blacklisting the associated
    token.

    Attributes:
        refresh: The refresh token provided for logout.
        default_error_message: A default message used to indicate errors.

    Methods:
        validate: Validates the provided attributes and extracts the refresh token.
        save: Saves the current object state by blacklisting the associated token.
    """

    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        """
        Validates the provided attributes and extracts the refresh token.

            This method retrieves the 'refresh' token from the given attributes
            and stores it in the instance variable `token`. It then returns the
            original attributes for further processing.

            Args:
                attrs: A dictionary containing the attributes to validate, which
                       must include a key 'refresh' with a corresponding token value.

            Returns:
                A dictionary containing the original attributes passed to the method.
        """
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """
        Save the current object state by blacklisting the associated token.

            This method attempts to blacklist the token associated with the
            RefreshToken instance. If the token cannot be blacklisted due to
            a TokenError, it calls the fail method with a 'bad_token' message.

            Args:
                **kwargs: Additional keyword arguments that may be used for
                          further configurations or data.

            Returns:
                None
        """

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")
