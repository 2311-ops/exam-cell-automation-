from django.contrib import admin
from marksheets.models import Marksheet

@admin.register(Marksheet)
class MarksheetAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'marks_obtained', 'total_marks', 'percentage', 'grade', 'result_status']
    list_filter = ['result_status', 'grade', 'created_at']
    search_fields = ['student__username', 'exam__name']
    readonly_fields = ['percentage', 'grade', 'result_status']
