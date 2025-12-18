from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

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
