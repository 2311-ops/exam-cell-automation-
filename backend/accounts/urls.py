from django.urls import path
from .views import RegisterView, login_view, MeView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),   # ← fix here
    path('me/', MeView.as_view(), name='me'),
]
