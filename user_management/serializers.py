from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User, SEX_CHOICES
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.gis.geos import fromstr


class CustumTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    A custom token obtain pair serializer that adds a custom claim to the token.
    """

    @classmethod
    def get_token(cls, user):
        """
        Override the get_token method to add a custom claim to the token.
        """
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        return token

  

  

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    sex = serializers.ChoiceField(choices=SEX_CHOICES, default='M')
    
    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'sex', 'date_of_birth')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'sex': {'required': False},
            'date_of_birth': {'required': False}
        }
    
    def validate(self, attrs):
        """
        Validates the input data before creating a new user.
    
        Args:
            attrs (dict): The input data to be validated, which includes the password and password confirmation fields.
        
        Returns:
            dict: The validated input data.
        
        Raises:
            serializers.ValidationError: If the password and password confirmation fields don't match.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        """
        Creates a new user object with the validated data. It also sets the user's password and sends a verification email.
    
        Args:
            validated_data (dict): The validated input data.
        
        Returns:
            User: The created user object.
        """
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            sex=validated_data.get('sex'),
            date_of_birth=validated_data.get('date_of_birth')
        )

        user.set_password(validated_data['password'])
        user.save()
        
        return user
