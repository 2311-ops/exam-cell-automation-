from django.contrib import admin
from students.models import StudentExamRegistration

@admin.register(StudentExamRegistration)
class StudentExamRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'registered_at', 'is_approved']
    list_filter = ['is_approved', 'registered_at']
    search_fields = ['student__username', 'exam__name']
    actions = ['approve_registration']

    def approve_registration(self, request, queryset):
        queryset.update(is_approved=True)
    approve_registration.short_description = "Approve selected registrations"
