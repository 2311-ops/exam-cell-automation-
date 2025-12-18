from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from halltickets.models import Exam, HallTicket
from marksheets.models import Marksheet
from students.models import StudentExamRegistration

from .serializers import (
    AdminUserSerializer,
    AdminExamSerializer,
    AdminStudentExamRegistrationSerializer,
    AdminHallTicketSerializer,
    AdminMarksheetSerializer,
)

User = get_user_model()


class AdminUserViewSet(viewsets.ModelViewSet):
    """Admin management for users (similar to Django admin list/edit)."""

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]


class AdminExamViewSet(viewsets.ModelViewSet):
    """Admin CRUD for exams."""

    queryset = Exam.objects.all().order_by("-exam_date")
    serializer_class = AdminExamSerializer
    permission_classes = [IsAdminUser]


class AdminRegistrationViewSet(viewsets.ModelViewSet):
    """Admin management of student exam registrations (approve, view)."""

    queryset = (
        StudentExamRegistration.objects.select_related("student", "exam")
        .all()
        .order_by("-registered_at")
    )
    serializer_class = AdminStudentExamRegistrationSerializer
    permission_classes = [IsAdminUser]


class AdminHallTicketViewSet(viewsets.ModelViewSet):
    """Admin CRUD for hall tickets."""

    queryset = HallTicket.objects.select_related("student", "exam").all().order_by(
        "-issued_at"
    )
    serializer_class = AdminHallTicketSerializer
    permission_classes = [IsAdminUser]


class AdminMarksheetViewSet(viewsets.ModelViewSet):
    """Admin CRUD for marksheets."""

    queryset = (
        Marksheet.objects.select_related("student", "exam")
        .all()
        .order_by("-created_at")
    )
    serializer_class = AdminMarksheetSerializer
    permission_classes = [IsAdminUser]


class EmailStudentsView(APIView):
    """
    Allow an admin to send an email to all registered students.

    Uses the EMAIL_* configuration from settings / .env.
    """

    permission_classes = [IsAdminUser]

    def post(self, request):
        subject = (request.data.get("subject") or "").strip()
        message = (request.data.get("message") or "").strip()

        if not subject or not message:
            return Response(
                {"detail": "Both subject and message are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # All users with role 'student' and a non-empty email
        recipients = list(
            User.objects.filter(role="student")
            .exclude(email__isnull=True)
            .exclude(email__exact="")
            .values_list("email", flat=True)
        )

        if not recipients:
            return Response(
                {"detail": "No student email addresses found."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        sent_count = send_mail(
            subject=subject,
            message=message,
            from_email=None,  # Use DEFAULT_FROM_EMAIL
            recipient_list=recipients,
            fail_silently=False,
        )

        return Response(
            {"detail": f"Email sent to {sent_count} students."},
            status=status.HTTP_200_OK,
        )
