from rest_framework import serializers
from halltickets.models import Exam, HallTicket

class ExamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'exam_date', 'duration_minutes', 'total_marks']


class HallTicketSerializer(serializers.ModelSerializer):
    exam = ExamDetailSerializer(read_only=True)
    student_username = serializers.CharField(source='student.username', read_only=True)

    class Meta:
        model = HallTicket
        fields = ['id', 'student_username', 'exam', 'roll_number', 'seat_number', 'room_number', 'invigilator_name', 'issued_at']
        read_only_fields = ['id', 'issued_at']
