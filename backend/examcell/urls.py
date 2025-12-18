from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts endpoints (register, login, me)
    path('api/accounts/', include('accounts.urls')),

    # Students endpoints (exams, halltickets, marksheets)
    path('api/students/', include('students.urls')),
]
