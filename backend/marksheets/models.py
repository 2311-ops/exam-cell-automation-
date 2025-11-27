from django.db import models
from django.contrib.auth import get_user_model
<<<<<<< HEAD
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
=======
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
>>>>>>> 53a8404ef9bfe451dbb0d667faf5fbc46ccafefa
