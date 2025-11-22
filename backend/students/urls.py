from django.urls import path
from students.views import (
    RegisterExamView,
    ViewAvailableExamsView,
    ViewHallTicketView,
    ViewMarksheetView
)

app_name = 'students'

urlpatterns = [
    path('exams/register/', RegisterExamView.as_view(), name='register_exam'),
    path('exams/registered/', RegisterExamView.as_view(), name='registered_exams'),
    path('exams/available/', ViewAvailableExamsView.as_view(), name='available_exams'),
    path('hallticket/', ViewHallTicketView.as_view(), name='hall_tickets'),
    path('hallticket/<int:exam_id>/', ViewHallTicketView.as_view(), name='hall_ticket_detail'),
    path('marksheet/', ViewMarksheetView.as_view(), name='marksheets'),
    path('marksheet/<int:exam_id>/', ViewMarksheetView.as_view(), name='marksheet_detail'),
]
