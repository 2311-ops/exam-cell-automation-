from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=[('student', 'Student'), ('staff', 'Staff')], default='student')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def validate_username(self, value):
        # Accept the provided username (we derive it from the email local-part in the view).
        # Validate basic constraints: non-empty and uniqueness.
        if not value:
            raise serializers.ValidationError("Username cannot be empty.")

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")

        return value

    def validate_email(self, value):
        # Email validation: just ensure it's not empty and not already used
        if not value:
            raise serializers.ValidationError("Email cannot be empty.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'student')
        )
        return user

# Serializer for login remains the same
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required.")

        # Allow users to enter either their username (roll / staff id) or their full email.
        # If an email is provided, try authenticating with the local-part (username) as well.
        user = authenticate(username=username, password=password)
        if not user and '@' in (username or ''):
            # derive local part from email and try again
            local_part = username.split('@', 1)[0]
            user = authenticate(username=local_part, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

# User details serializer remains the same
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
