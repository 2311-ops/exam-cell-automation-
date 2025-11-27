from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from emailservice.utils import send_welcome_email  # make sure emailservice exists

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Send welcome email (best-effort)
        try:
            send_welcome_email(user.email, user.username)
            email_msg = "User registered and welcome email sent."
        except Exception:
            # ensure registration succeeds even if email sending fails
            email_msg = "User registered but welcome email failed to send."

        return Response(
            {"message": email_msg},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'Login successful',
                'access': serializer.validated_data['access'],
                'refresh': serializer.validated_data['refresh'],
                'username': serializer.validated_data['username'],
                'role': serializer.validated_data['role'],
                'user_id': user.id,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
