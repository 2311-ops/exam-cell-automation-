from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student

User = get_user_model()

class Exam(models.Model):
    name = models.CharField(max_length=255)
    course_code = models.CharField(max_length=50)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.course_code})"


class ExamRoom(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField(default=30)
    occupied_seats = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Room {self.room_number} ({self.occupied_seats}/{self.capacity})"


class HallTicket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    exam_room = models.ForeignKey(ExamRoom, on_delete=models.SET_NULL, null=True, blank=True)
    seat_no = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issue_date = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('student', 'exam')
    
    def __str__(self):
        return f"HT({self.student.user.username} - {self.exam.course_code})"
