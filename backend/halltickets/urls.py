from django.urls import path
<<<<<<< HEAD
from halltickets.views import ExamViewSet, ExamRoomViewSet, HallTicketViewSet
from marksheets.views import MarkViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'rooms', ExamRoomViewSet, basename='room')
router.register(r'halltickets', HallTicketViewSet, basename='hallticket')
router.register(r'marks', MarkViewSet, basename='mark')

urlpatterns = router.urls
=======

app_name = 'halltickets'

urlpatterns = [
    # Halltickets are accessed via students app
]
>>>>>>> 53a8404ef9bfe451dbb0d667faf5fbc46ccafefa
