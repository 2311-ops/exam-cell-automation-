from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from emailservice.utils import send_welcome_email  # make sure this exists

User = get_user_model()


# -------------------------
# Register a new user
# -------------------------
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
            email_msg = "User registered but welcome email failed to send."

        return Response(
            {"message": email_msg},
            status=status.HTTP_201_CREATED
        )


# -------------------------
# Login existing user
# -------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        # Login user using Django session (optional if using JWT only)
        login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        return Response({
            "message": "Login successful",
            "access": str(access),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


# -------------------------
# Get logged-in user details
# -------------------------
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
