from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts endpoints (register, login, me)
    path('api/accounts/', include('accounts.urls')),

    # Students endpoints (exams, halltickets, marksheets)
    path('api/students/', include('students.urls')),

    # Admin panel API (custom admin dashboard)
    path('api/admin/', include('adminpanel.urls')),

    # Email service
    path('api/emails/', include('emailservice.urls')),
]
