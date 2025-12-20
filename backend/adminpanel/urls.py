from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdminUserViewSet,
    AdminExamViewSet,
    AdminRegistrationViewSet,
    AdminHallTicketViewSet,
    AdminMarksheetViewSet,
    EmailStudentsView,
)

router = DefaultRouter()
router.register(r"users", AdminUserViewSet, basename="admin-users")
router.register(r"exams", AdminExamViewSet, basename="admin-exams")
router.register(r"registrations", AdminRegistrationViewSet, basename="admin-registrations")
router.register(r"halltickets", AdminHallTicketViewSet, basename="admin-halltickets")
router.register(r"marksheets", AdminMarksheetViewSet, basename="admin-marksheets")

urlpatterns = [
    path("", include(router.urls)),
    path("email/students/", EmailStudentsView.as_view(), name="admin-email-students"),
]
