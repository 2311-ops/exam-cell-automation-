from django.db import models
from django.contrib.auth.models import AbstractUser

class user(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
    )
    #adding new column role to the default user model
    role = models.CharField(max_length=10, choices=ROLE_CHOICES  , default='student')
    #defines string representation of the user model
    def __str__(self):
        return f"{self.username}, {self.role}"
