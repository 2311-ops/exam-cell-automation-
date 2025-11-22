from django.db import models
from django.contrib.auth import get_user_model
from students.models import Student
from halltickets.models import Exam
from decimal import Decimal

User = get_user_model()

class Mark(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, default='Exam')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, default='F')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('student', 'exam')
    
    def save(self, *args, **kwargs):
        # Calculate grade based on score
        score_float = float(self.score)
        if score_float >= 90:
            self.grade = 'A'
        elif score_float >= 80:
            self.grade = 'B'
        elif score_float >= 70:
            self.grade = 'C'
        elif score_float >= 60:
            self.grade = 'D'
        else:
            self.grade = 'F'
        
        super().save(*args, **kwargs)
        
        # Update student GPA
        self.student.calculate_gpa()
    
    def __str__(self):
        return f"Mark({self.student.user.username} - {self.exam.course_code}: {self.score})"
