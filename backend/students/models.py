from django.db import models
from django.contrib.auth import get_user_model
<<<<<<< HEAD

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    
    def __str__(self):
        return f"Student({self.user.username})"
    
    def calculate_gpa(self):
        from marksheets.models import Mark
        marks = Mark.objects.filter(student=self)
        if not marks.exists():
            self.gpa = 0.0
        else:
            total_score = sum(float(m.score) for m in marks)
            avg_score = total_score / marks.count()
            self.gpa = round(avg_score / 100 * 4, 2)
        self.save()
        return self.gpa
=======
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
>>>>>>> bd48eb6f41dc796d9e2a255bfcb996ed6fc8157e
