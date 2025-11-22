from django.db import models
from django.contrib.auth import get_user_model

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
