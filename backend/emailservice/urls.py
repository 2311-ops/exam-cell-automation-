from django.urls import path
from .views import send_test_email, send_email_to_admin

urlpatterns = [
    path('send-test/', send_test_email, name='send-test-email'),
    path('contact-admin/', send_email_to_admin, name='send-email-to-admin'),
]
