from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from marksheets.models import Mark
from marksheets.serializers import MarkSerializer
from students.models import Student


class MarkViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MarkSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        student = Student.objects.get(user=self.request.user)
        return Mark.objects.filter(student=student)
