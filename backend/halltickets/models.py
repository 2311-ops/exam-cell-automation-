from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Exam(models.Model):
    """Model to store exam information"""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    exam_date = models.DateTimeField()
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return self.name


class HallTicket(models.Model):
    """Model to store hall ticket information for students"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hall_tickets')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='hall_tickets')
    roll_number = models.CharField(max_length=50, unique=True)
    seat_number = models.CharField(max_length=50)
    room_number = models.CharField(max_length=50)
    invigilator_name = models.CharField(max_length=255, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-issued_at']

    def __str__(self):
        return f"Hall Ticket - {self.student.username} ({self.roll_number})"
