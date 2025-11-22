from django.db import models
from django.contrib.auth import get_user_model
from halltickets.models import Exam

User = get_user_model()

class StudentExamRegistration(models.Model):
    """Model to track which exams a student is registered for"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_registrations')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='student_registrations')
    registered_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.student.username} - {self.exam.name}"
