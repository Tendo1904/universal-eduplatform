from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy as _

class LoginSerializer(TokenObtainPairSerializer):
    """
    A class representing a serializer for handling login data.
    
        Class Methods:
        - validate: Validate the data provided for login.
        - save: Save the login data into the database.
    """

    def get_token(self, user):
        """
        Get the authentication token for the given user by adding custom claims.
        
        Args:
        - self: The instance of the class.
        - user: The user object for which the token is requested.
        
        Returns:
        Dictionary: A dictionary containing the authentication token with added custom claims including username and role.
        """
        token = super().get_token(user)
        
        # Add custom claims
        token['username'] = user.username
        token['role'] = user.role
        
        return token
    
class SignInSerializer(serializers.ModelSerializer):
    """
    A serializer class for validating and processing user sign-in data.
    
        Attributes:
            - username: The username provided by the user.
            - password: The password provided by the user.
    
        The SignInSerializer class provides methods to validate the sign-in data provided by the user and process it accordingly.
    """

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active']
        
class RegistrationSerializer(serializers.ModelSerializer):
    """
    This class represents a serializer for user registration data.
    
        Class Attributes:
        - email: The email address of the user.
        - password: The password for the user account.
    
        Class Methods:
        - create: This method is responsible for creating a new user account.
    """


    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    @classmethod
    def create(self, validated_data):
        """
        Creates a new user instance using the provided validated data.
        
        Args:
        - validated_data (dict): A dictionary containing the data to create the user object.
        
        Returns:
        User: The newly created user object.
        """
        return User.objects.create_user(**validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    """
    This class provides functionality to serialize user data.
    
        Attributes:
            username: The username of the user.
            email: The email address of the user.
    
        Methods:
            serialize_user_data: Serialize the user data for output.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'role']

class LogoutSerializer(serializers.Serializer):
    """
    Serialize logout requests.
    
        Class Attributes:
        - None
    
        Class Methods:
        - validate: Validates the data for logout requests.
        - save: Saves the data for logout requests.
    """

    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        """
        Validate the attributes by assigning the 'refresh' token from the provided dictionary.
        
        Args:
        - self: The instance of the class.
        - attrs: A dictionary containing attributes to validate.
        
        Returns:
        A dictionary representing the validated attributes.
        """
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        """
        Save the token by blacklisting it if necessary.
        
        Args:
        - self: The instance of the class.
        - **kwargs: additional keyword arguments
        
        Return:
        None
        """

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')

