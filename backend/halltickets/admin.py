from django.contrib import admin
from halltickets.models import Exam, HallTicket

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam_date', 'duration_minutes', 'total_marks']
    list_filter = ['exam_date']
    search_fields = ['name']

@admin.register(HallTicket)
class HallTicketAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'roll_number', 'seat_number', 'room_number']
    list_filter = ['exam', 'issued_at']
    search_fields = ['student__username', 'exam__name', 'roll_number']
