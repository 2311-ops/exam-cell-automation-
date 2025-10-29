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
        #create_user() handles password hashing and user creation
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        user.save()
        return user
        
#serializer for user login
class LoginSerializer(serializers.Serializer):
    #provided by the client
    username = serializers.CharField()
    #provided by the client
    password = serializers.CharField(write_only=True)
    #returned by the server upon successful login
    access = serializers.CharField(read_only=True)    
    #returned by the server upon successful login
    refresh = serializers.CharField(read_only=True)
    
    #validate method to authenticate user and generate tokens
    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid username or password")
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
#shows user details
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']