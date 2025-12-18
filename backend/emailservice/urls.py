from django.urls import path
from .views import send_test_email

urlpatterns = [
    path('send-test/', send_test_email, name='send-test-email'),
]
