from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from emailservice.utils import send_welcome_email

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Prefer an explicit username provided by the user; fall back to the
        # local-part of the email (before @) only when no username is supplied.
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        provided_username = data.get('username')
        if provided_username and str(provided_username).strip():
            username = str(provided_username).strip()
        else:
            # derive username from email local-part
            username = email.split('@')[0]

        # Build data for the serializer with the chosen username so validation uses it
        data['username'] = username

        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        # Save user (serializer will use the computed username)
        user = serializer.save()

        # Send welcome email (send_welcome_email returns True on success, False on failure)
        try:
            sent = send_welcome_email(user.email, user.username)
            if sent:
                email_msg = "User registered and welcome email sent."
            else:
                email_msg = "User registered but welcome email failed (check server logs)."
        except Exception as e:
            # In case send_welcome_email unexpectedly raises
            email_msg = f"User registered but welcome email failed: {e}"

        # Return response
        return Response(
            {"message": email_msg, "user": UserSerializer(user).data},
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            'message': 'Login successful',
            'access': str(access),
            'refresh': str(refresh),
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
