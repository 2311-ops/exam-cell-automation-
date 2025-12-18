from django.db import models
from django.contrib.auth import get_user_model
from halltickets.models import Exam

User = get_user_model()

class Marksheet(models.Model):
    """Model to store student marks for exams"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marksheets')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marksheets')
    marks_obtained = models.FloatField()
    total_marks = models.FloatField()
    percentage = models.FloatField(blank=True, null=True)
    grade = models.CharField(max_length=2, blank=True)
    result_status = models.CharField(
        max_length=10,
        choices=[('PASS', 'Pass'), ('FAIL', 'Fail'), ('PENDING', 'Pending')],
        default='PENDING'
    )
    published_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """Automatically calculate percentage and grade on save"""
        if self.total_marks > 0:
            self.percentage = (self.marks_obtained / self.total_marks) * 100
            # Simple grading logic
            if self.percentage >= 80:
                self.grade = 'A'
            elif self.percentage >= 70:
                self.grade = 'B'
            elif self.percentage >= 60:
                self.grade = 'C'
            elif self.percentage >= 50:
                self.grade = 'D'
            else:
                self.grade = 'F'
                self.result_status = 'FAIL'
            
            if self.percentage >= 50 and self.result_status != 'FAIL':
                self.result_status = 'PASS'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Marksheet - {self.student.username} ({self.exam.name})"
