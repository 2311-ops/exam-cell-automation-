#serializer handling user registration, login, and user details 
from rest_framework import serializers
#retrieve the custom user model
from django.contrib.auth import get_user_model
#create JWT tokens for user
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    #adding serializer for user registration and hide it from responses
    password = serializers.CharField(write_only=True)
    #meta tells serializer which model to use and which fields to include
    class Meta:
        #user model retured by get_user_model()
        model = User
        #fields to include in the serializer
        fields = ['username', 'email', 'password', 'role']
    #create method to create a new user instance
    def create(self, validated_data):
        # create_user() handles password hashing and user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        return user
        
#serializer for user login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username:
            raise serializers.ValidationError({'username': 'This field is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'This field is required.'})

        # Authenticate with username and password only
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not getattr(user, 'is_active', True):
            raise serializers.ValidationError('User account is disabled')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'role': user.role
        }
#shows user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
